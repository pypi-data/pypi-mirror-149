import io
import sys
import grpc
import logging
import argparse
import numpy as np
from PIL import Image
from io import BytesIO
from functools import partial
from concurrent import futures
import tritonclient.grpc as grpcclient
import tritonclient.http as httpclient

from afilter.protos import afilter_pb2
from afilter.protos import afilter_pb2_grpc
from afilter.utils.check_health import HealthServicer
from tritonclient.utils import InferenceServerException

try:
    from mmseg.datasets.vsp_cam import VSP_CAMDataset
    CLASSES = VSP_CAMDataset.CLASSES
except Exception as e:
    CLASSES = ('background', 'island', 'nick', 'open', 'protrusion', 'short')

if sys.version_info >= (3, 0):
    import queue
else:
    import Queue as queue

OK = True
NG = False

# Callback function used for async_stream_infer()
def completion_callback(user_data, result, error):
    # passing error raise and handling out
    user_data._completed_requests.put((result, error))

class UserData:

    def __init__(self):
        self._completed_requests = queue.Queue()

user_data = UserData()

def get_class_mask(defect):
    classes = np.array(CLASSES)

    class_mask = []
    for label, name in enumerate(classes):
        if label != 0 and name != '':
            table = [0]*256
            table[label] = 1
            mask = defect.point(table, '1')
            if mask.getextrema() != (0, 0):
                print('[{}]: {}'.format(label, name))
                mask_bytes = BytesIO()
                mask.save(mask_bytes, format='png')
                mask_Onemat = afilter_pb2.Onemat(rows=mask.size[1], cols=mask.size[0], d_type=0, mat_data=mask_bytes.getvalue())
                class_mask.append(afilter_pb2.Onedefect(name=name, mask=mask_Onemat))

    return class_mask

def get_concat(cam_data, cad_data):
    # cam = Image.frombytes(mode="RGBA", size=(cam_data.rows,cam_data.cols), data=cam_data.mat_data, decoder_name="raw")
    cam = Image.open(io.BytesIO(cam_data.mat_data))
    cam = cam.resize((600, 600), Image.ANTIALIAS)
    # cam = cam.convert("RGB")
    cam = np.asarray(cam)
    cam = cam / 255
    cam = np.expand_dims(cam, axis=0)
    cam = np.transpose(cam, axes=[0, 3, 1, 2])
    cam = cam.astype(np.float32)

    # cad = Image.frombytes(mode="RGBA", size=(cad_data.rows,cad_data.cols), data=cad_data.mat_data, decoder_name="raw").convert('L')
    cad = Image.open(io.BytesIO(cad_data.mat_data)).convert('L')
    cad = cad.resize((600, 600), Image.ANTIALIAS)
    cad = np.asarray(cad)
    cad = cad / 255
    cad = np.expand_dims(cad, axis=0)
    cad = np.expand_dims(cad, axis=0)
        
    cam_cad = np.append(cam, cad, axis = 1)
    return cam_cad.astype(np.float32)

def get_defects(protocol, triton_client, model_name, requests, set_async):
    REQ_NUM = len(requests)
    inputs_data = [get_concat(request.cam_data, request.cad_data) for request in requests]
    outputs_data = []
    try:
        if protocol =='grpc':
            inputs = [[grpcclient.InferInput(f'input', [1, 4, 600, 600], "FP32")] for i in range(REQ_NUM)]
            [inputs[i][0].set_data_from_numpy(inputs_data[i]) for i in range(REQ_NUM)]
            outputs = [[grpcclient.InferRequestedOutput(f'output')] for i in range(REQ_NUM)]
            if set_async:
                [triton_client.async_infer(model_name=model_name,
                                            inputs=inputs[i],
                                            callback=partial(completion_callback, user_data),
                                            outputs=outputs[i]) for i in range(REQ_NUM)]
                # outputs_data=user_data._completed_requests.get()
                processed_count = 0
                while processed_count < REQ_NUM:
                    (response, error) = user_data._completed_requests.get()
                    processed_count += 1
                    if error is not None:
                        print("Triton gRCP inference failed: " + str(error))
                        sys.exit(1)
                    outputs_data.append(response)
                # results = [output_data.as_numpy('output') for output_data in outputs_data]
            else:
                outputs_data = [triton_client.infer(model_name=model_name,
                                                    inputs=inputs[i],
                                                    outputs=outputs[i]) for i in range(REQ_NUM)]
        else:
            inputs = [[httpclient.InferInput('input', [1, 4, 600, 600], "FP32")] for i in range(REQ_NUM)]
            [inputs[i][0].set_data_from_numpy(inputs_data[i], binary_data=True) for i in range(REQ_NUM)]
            outputs = [[httpclient.InferRequestedOutput('output', binary_data=True)] for i in range(REQ_NUM)]
            if set_async:
                async_outputs = [triton_client.async_infer(model_name=model_name,
                                                        inputs=inputs[i],
                                                        outputs=outputs[i]) for i in range(REQ_NUM)]
                [outputs_data.append(async_output.get_result()) for async_output in async_outputs]
            else:
                outputs_data = [triton_client.infer(model_name=model_name,
                                                    inputs=inputs[i],
                                                    outputs=outputs[i]) for i in range(REQ_NUM)]
        results = [output_data.as_numpy('output') for output_data in outputs_data]
    except InferenceServerException as e:
            print("inference failed: " + str(e))
            sys.exit(1)

    return [Image.fromarray(np.squeeze(result.astype('uint8')), mode='L') for result in results]

def get_OKNG(defect):
    class_mask = get_class_mask(defect)
    if class_mask == ([] or None):
        return afilter_pb2.OneReply(ok_ng=OK)
    else:
        return afilter_pb2.OneReply(ok_ng=NG, defect=class_mask)


class FilterServicer(afilter_pb2_grpc.FilterServicer, HealthServicer):
    def __init__(self,
                 protocol,
                 url,
                 model_name,
                 set_async = True):
        self.protocol = protocol
        self.url = url
        self.model_name = model_name
        self.set_async = set_async
        try:
            if self.protocol.lower() == "grpc":
                self.triton_client = grpcclient.InferenceServerClient(url=self.url+':8001')
            else:
                self.triton_client = httpclient.InferenceServerClient(url=self.url+':8000',
                    concurrency=100 if self.set_async == True else 1)
        except Exception as e:
            print("context creation failed: " + str(e))
            sys.exit()

        super(FilterServicer, self).__init__()

    def FilterFunc(self, requests, context):
        reply = []
        # REQ_NUM = len(requests.request)

        defects = get_defects(self.protocol.lower(), self.triton_client, 
                              self.model_name, requests.request, set_async = True)
        for defect in defects:
            reply.append(get_OKNG(defect))
        return afilter_pb2.FilterReply(reply=reply)
    
    def FilterCheck(self, request, context):
        response = self.Check(request, context)
        if response.status == afilter_pb2.HealthCheckResponse.SERVING:
            server_live = self.triton_client.is_server_live()
            server_ready = self.triton_client.is_server_ready()
            model_ready = self.triton_client.is_model_ready(self.model_name)
            if server_live and server_ready and model_ready:
                return afilter_pb2.HealthCheckResponse(status=afilter_pb2.HealthCheckResponse.SERVING)
            else:
                return afilter_pb2.HealthCheckResponse(status=afilter_pb2.HealthCheckResponse.NOT_SERVING)
        else:
            return response

def aivs_serve(protocol, url, model_name):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    afilter_pb2_grpc.add_FilterServicer_to_server(
        FilterServicer(protocol, url, model_name, set_async = True), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u',
        '--triton_url',
        type=str,
        required=False,
        default='localhost',
        help='Inference server URL. Default is localhost.')
    parser.add_argument('-i',
        '--protocol',
        type=str,
        required=False,
        default='gRPC',
        help='Protocol (HTTP/gRPC) used to communicate with ' +
        'the inference service. Default is HTTP.')
    parser.add_argument('--model_name', default='segformer-b2', help='The model name in the server')
    args = parser.parse_args()

    logging.basicConfig()
    aivs_serve(args.protocol, args.triton_url, args.model_name)
