# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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
Preprocessing tools for ImageNet dataset.
"""

import numpy as np
import tensorflow as tf

from .imagenet_labels2names import imagenet_labels


@tf.function
def preprocess_image(image, image_size, training=False):
    """ ImageNet data preprocessing.

    Preprocessing includes cropping, and resizing for both training and
    validation images. Training preprocessing introduces some random distortion
    of the image to improve accuracy.

    Args:
        image (tf.Tensor): input image as a 3-D tensor
        image_size (int): desired image size
        training (bool, optional): True for training preprocessing, False for
            validation and inference. Defaults to False.
    """
    shape = tf.shape(image)

    if training:
        # For training: crop, flip and resize
        bbox_begin, bbox_size, _ = tf.image.sample_distorted_bounding_box(
            shape,
            tf.zeros([0, 0, 4], tf.float32),  # force using whole image
            use_image_if_no_bounding_boxes=True,
            min_object_covered=0.1,
            aspect_ratio_range=[0.75, 1.33],
            area_range=[0.05, 1.0],
            max_attempts=100)

        image = tf.slice(image, bbox_begin, bbox_size)
        image = tf.image.random_flip_left_right(image)
        image = tf.image.resize(image, (image_size, image_size))
    else:
        # For validation/inference: aspect preserving resize and central crop
        height = tf.cast(shape[0], tf.float32)
        width = tf.cast(shape[1], tf.float32)

        resize_min = np.round(image_size * 1.143).astype(np.float32)
        scale_ratio = resize_min / tf.minimum(height, width)

        # Convert back to int for TF ops
        new_height = tf.cast(height * scale_ratio, tf.int32)
        new_width = tf.cast(width * scale_ratio, tf.int32)

        image = tf.image.resize(image, [new_height, new_width])

        # Second: central crop to desired image_size
        image = tf.image.resize_with_crop_or_pad(image, image_size, image_size)

    return tf.cast(image, tf.float32)


def index_to_label(index):
    """ Function to get an ImageNet label from an index.

    Args:
        index: between 0 and 999

    Returns:
        str: a string of coma separated labels
    """
    return imagenet_labels[index]
