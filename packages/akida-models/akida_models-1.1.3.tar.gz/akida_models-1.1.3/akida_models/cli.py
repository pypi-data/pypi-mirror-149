#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
akida_models main command-line interface

This package entry-point allows akida models to be instantiated and saved at a
specified location.

"""

import argparse

from .utk_face.model_vgg import vgg_utk_face
from .kws.model_ds_cnn import ds_cnn_kws
from .modelnet40.model_pointnet_plus import pointnet_plus_modelnet40
from .imagenet.model_mobilenet import mobilenet_imagenet
from .imagenet.model_vgg import vgg_imagenet
from .imagenet.model_akidanet import akidanet_imagenet
from .imagenet.model_akidanet_edge import akidanet_edge_imagenet
from .imagenet.model_mobilenet_edge import mobilenet_edge_imagenet
from .detection.model_yolo import yolo_base
from .dvs.model_convtiny_handy import convtiny_dvs_handy
from .dvs.model_convtiny_gesture import convtiny_dvs_gesture
from .cwru.model_convtiny import convtiny_cwru
from .mnist.model_gxnor import gxnor_mnist


def main():
    """ CLI entry point.

    Contains an argument parser with specific arguments depending on the model
    to be created. Complete arguments lists available using the -h or --help
    argument.

    """
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest="action")
    c_parser = sp.add_parser("create", help="Create an akida Keras model")
    c_parser.add_argument("-s",
                          "--save_model",
                          type=str,
                          default=None,
                          help="The path/name to use to save the model")
    csp = c_parser.add_subparsers(dest="model",
                                  help="The type of model to be instantiated")
    csp.add_parser("vgg_utk_face", help="A VGG-like UTKFace model")
    csp.add_parser("convtiny_dvs_handy", help="A Convtiny DVS handy model")
    dvsh_parser = csp.add_parser("convtiny_dvs_handy",
                                 help="A Convtiny DVS model for akida")
    dvsh_parser.add_argument("-c",
                             "--classes",
                             type=int,
                             default=9,
                             help="The number of classes")
    csp.add_parser("convtiny_dvs_gesture", help="A Convtiny DVS gesture model")
    dvsg_parser = csp.add_parser("convtiny_dvs_gesture",
                                 help="A Convtiny DVS model for akida")
    dvsg_parser.add_argument("-c",
                             "--classes",
                             type=int,
                             default=10,
                             help="The number of classes")
    csp.add_parser(
        "ds_cnn_kws",
        help="A Depthwise Separable MobileNet-like model for the Keyword"
        " Spotting example")
    mb_parser = csp.add_parser("mobilenet_imagenet",
                               help="A MobileNet V1 model for akida")
    image_sizes = [32, 64, 96, 128, 160, 192, 224]
    mb_parser.add_argument("-i",
                           "--image_size",
                           type=int,
                           default=224,
                           choices=image_sizes,
                           help="The square input image size")
    mb_parser.add_argument("-a",
                           "--alpha",
                           type=float,
                           default=1.0,
                           help="The width of the model")
    mb_parser.add_argument("-c",
                           "--classes",
                           type=int,
                           default=1000,
                           help="The number of classes")
    vgg_parser = csp.add_parser("vgg_imagenet", help="A VGG model for akida")
    vgg_parser.add_argument("-c",
                            "--classes",
                            type=int,
                            default=1000,
                            help="The number of classes")
    mbe_parser = csp.add_parser("mobilenet_imagenet_edge",
                                help="A MobileNet V1 model modified for akida \
                                edge learning")
    mbe_parser.add_argument("-bm",
                            "--base_model",
                            type=str,
                            required=True,
                            help="The base MobileNet model to use for edge \
                            adaptation.")
    mbe_parser.add_argument("-c",
                            "--classes",
                            type=int,
                            default=1000,
                            help="The number of edge learning classes")
    an_parser = csp.add_parser("akidanet_imagenet", help="An AkidaNet model")
    an_parser.add_argument("-i",
                           "--image_size",
                           type=int,
                           default=224,
                           choices=image_sizes,
                           help="The square input image size")
    an_parser.add_argument("-a",
                           "--alpha",
                           type=float,
                           default=1.0,
                           help="The width of the model")
    an_parser.add_argument("-c",
                           "--classes",
                           type=int,
                           default=1000,
                           help="The number of classes")
    ane_parser = csp.add_parser("akidanet_edge_imagenet",
                                help="An AkidaNet model modified for akida \
                                edge learning")
    ane_parser.add_argument("-bm",
                            "--base_model",
                            type=str,
                            required=True,
                            help="The base AkidaNet model to use for edge \
                            adaptation.")
    ane_parser.add_argument("-c",
                            "--classes",
                            type=int,
                            default=1000,
                            help="The number of edge learning classes")
    pnet_parser = csp.add_parser("pointnet_plus_modelnet40",
                                 help="A PointNet++ model for Akida")
    pnet_parser.add_argument("-c",
                             "--classes",
                             type=int,
                             default=40,
                             help="The number of classes")
    pnet_parser.add_argument("-alpha",
                             "--alpha",
                             type=float,
                             default=1.0,
                             help="Network filters multiplier (typically 0.5 , \
                             [1.0]")
    yl_parser = csp.add_parser("yolo_base", help="A YOLOv2 model for detection")
    yl_parser.add_argument("-c",
                           "--classes",
                           type=int,
                           default=1,
                           help="The number of classes")
    yl_parser.add_argument("-na",
                           "--number_anchors",
                           type=int,
                           default=5,
                           help="The number of anchor boxes")
    yl_parser.add_argument("-a",
                           "--alpha",
                           type=float,
                           default=0.5,
                           help="The width of the model")
    yl_parser.add_argument("-bw",
                           "--base_weights",
                           type=str,
                           default=None,
                           help="The base MobileNet weights to use for \
                            transfer learning.")
    csp.add_parser("convtiny_cwru", help="A Convtiny CWRU model for akida")
    csp.add_parser("gxnor_mnist", help="A GXNOR MNIST model for akida")
    args = parser.parse_args()
    if args.action == "create":
        # Instantiate the wished model
        if args.model == "vgg_utk_face":
            model = vgg_utk_face()
        elif args.model == "convtiny_dvs_handy":
            model = convtiny_dvs_handy(classes=args.classes)
        elif args.model == "convtiny_dvs_gesture":
            model = convtiny_dvs_gesture(classes=args.classes)
        elif args.model == "ds_cnn_kws":
            model = ds_cnn_kws()
        elif args.model == "pointnet_plus_modelnet40":
            model = pointnet_plus_modelnet40(alpha=args.alpha,
                                             classes=args.classes)
        elif args.model == "mobilenet_imagenet":
            input_shape = (args.image_size, args.image_size, 3)
            model = mobilenet_imagenet(input_shape,
                                       alpha=args.alpha,
                                       classes=args.classes)
        elif args.model == "vgg_imagenet":
            model = vgg_imagenet(classes=args.classes)
        elif args.model == "mobilenet_imagenet_edge":
            model = mobilenet_edge_imagenet(base_model=args.base_model,
                                            classes=args.classes)
        elif args.model == "akidanet_imagenet":
            input_shape = (args.image_size, args.image_size, 3)
            model = akidanet_imagenet(input_shape,
                                      alpha=args.alpha,
                                      classes=args.classes)
        elif args.model == "akidanet_edge_imagenet":
            model = akidanet_edge_imagenet(base_model=args.base_model,
                                           classes=args.classes)
        elif args.model == "yolo_base":
            model = yolo_base(classes=args.classes,
                              nb_box=args.number_anchors,
                              alpha=args.alpha)
            if args.base_weights is not None:
                model.load_weights(args.base_weights, by_name=True)
        elif args.model == "convtiny_cwru":
            model = convtiny_cwru()
        elif args.model == "gxnor_mnist":
            model = gxnor_mnist()
        # No need for default behaviour as the command-line parser only accepts
        # valid model types
        model_path = args.save_model
        if model_path is None:
            model_path = \
                f"{model.name}.h5" if args.model in (
                    "mobilenet_imagenet", "mobilenet_imagenet_edge") else f"{args.model}.h5"

        # If needed, add the extension
        if not model_path.endswith(".h5"):
            model_path = f"{model_path}.h5"
        model.save(model_path, include_optimizer=False)
        print(f"Model saved as {model_path}")
