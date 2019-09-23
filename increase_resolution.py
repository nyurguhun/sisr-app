#!/usr/bin/env python3
"""
 Copyright (C) 2018-2019 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
from __future__ import print_function
import sys
import os
from argparse import ArgumentParser, SUPPRESS
import numpy as np
import cv2
import logging as log
from time import time
from openvino.inference_engine import IENetwork, IECore
from PIL import Image


def generate_upsample_file(original_image_path, scale_factor, upsampled_file_name):
    image = cv2.imread(str(original_image_path))
    upsampled_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(str(original_image_path.parent / upsampled_file_name), upsampled_image)

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument("-m", "--model", help="Required. Path to an .xml file with a trained model",
                      required=True, type=str)
    args.add_argument("-i", "--input", help="Required. Path to a folder with images or path to an image files",
                      required=True, type=str, nargs="+")
    args.add_argument("-l", "--cpu_extension",
                      help="Optional. Required for CPU custom layers. "
                           "Absolute MKLDNN (CPU)-targeted custom layers. Absolute path to a shared library with the "
                           "kernels implementations", type=str, default=None)
    args.add_argument("-d", "--device",
                      help="Optional. Specify the target device to infer on; CPU, GPU, FPGA, HDDL or MYRIAD is "
                           "acceptable. Sample will look for a suitable plugin for device specified. Default value is CPU",
                      default="CPU", type=str)
    args.add_argument("-nt", "--number_top", help="Optional. Number of top results", default=10, type=int)
    return parser


def main():
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
    args = build_argparser().parse_args()
    model_xml = args.model
    model_bin = os.path.splitext(model_xml)[0] + ".bin"

    log.info("Creating Inference Engine")
    ie = IECore()
    if args.cpu_extension and 'CPU' in args.device:
        ie.add_extension(args.cpu_extension, "CPU")
    # Read IR
    log.info("Loading network files:\n\t{}\n\t{}".format(model_xml, model_bin))
    net = IENetwork(model=model_xml, weights=model_bin)

    if "CPU" in args.device:
        supported_layers = ie.query_network(net, "CPU")
        not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        if len(not_supported_layers) != 0:
            log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      format(args.device, ', '.join(not_supported_layers)))
            log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                      "or --cpu_extension command line argument")
            sys.exit(1)
    assert len(net.inputs.keys()) == 2, "Sample supports only single input topologies"
    assert len(net.outputs) == 1, "Sample supports only single output topologies"

    log.info("Preparing input blobs")
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    net.batch_size = len(args.input)

    # Read and pre-process input images
    n, c, h, w = net.inputs[input_blob].shape
    log.info(net.inputs)
    log.info(net.outputs[out_blob].shape)

    original_image = cv2.imread(args.input[0])
    log.info("shape of original image: {}".format(original_image.shape))
    #CHANGE THIS TO REMOVE HARDCODING
    original_image = cv2.resize(original_image, (480, 270))

    transposed_image = np.transpose(original_image, (2, 0, 1))

    upsampled_file_name = "upsampled.jpg"

    upsampled_dsize = (1920, 1080)
    upsampled_image = cv2.resize(original_image, upsampled_dsize, interpolation=cv2.INTER_CUBIC)
    transposed_upsampled_image = np.transpose(upsampled_image, (2, 0, 1))
    log.info("shape of upsampled image: {}".format(upsampled_image.shape))

    log.info("Batch size is {}".format(n))

    # Loading model to the plugin
    log.info("Loading model to the plugin")
    exec_net = ie.load_network(network=net, device_name=args.device)

    # Start sync inference
    log.info("Starting inference")
    images = {'0': np.expand_dims(transposed_image, axis=0),  
              '1': np.expand_dims(transposed_upsampled_image, axis=0)}
    res = exec_net.infer(inputs=images)

    # Processing output blob
    log.info("Processing output blob")
    res = res[out_blob][0]
    res *= 255
    res = np.clip(res, 0., 255.)
    res = res.transpose((1, 2, 0)).astype(np.uint8)

    out_img = os.path.join(os.path.dirname(__file__), "output.jpg")
    cv2.imwrite(out_img, res)

    log.info("Result image was saved to {}".format(out_img))


if __name__ == '__main__':
    sys.exit(main() or 0)
