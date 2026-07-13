import os
import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input

MODELS = {

    "custom_cnn": {
        "path": "models/custom_cnn_best.keras",
        "layer": "conv2d_3",
        "size": (256, 256)
    },

    "densenet121": {
        "path": "models/densenet121_best.keras",
        "layer": "conv5_block16_concat",
        "size": (256, 256)
    },

    "efficientnetb4": {
        "path": "models/efficientnetb4_best.keras",
        "layer": "top_conv",
        "size": (380, 380)
    },

    "resnet50": {
        "path": "models/resnet50_v2_best.keras",
        "layer": "conv5_block3_out",
        "size": (256, 256)
    },

    "tbnet": {
        "path": "models/tbnet_best.keras",
        "layer": "conv5_block3_out",
        "size": (256, 256)
    }
}

loaded_models = {}


def get_model(model_name):

    if model_name not in loaded_models:

        loaded_models[model_name] = load_model(
            MODELS[model_name]["path"],
            compile=False
        )

    return loaded_models[model_name]


def get_heatmap(img_array, model, layer_name):

    grad_model = tf.keras.models.Model(
        [model.inputs],
        [
            model.get_layer(layer_name).output,
            model.output
        ]
    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)

        loss = predictions[:, 0]

    grads = tape.gradient(
        loss,
        conv_outputs
    )

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = tf.reduce_sum(
        pooled_grads * conv_outputs,
        axis=-1
    )

    heatmap = np.maximum(
        heatmap,
        0
    )

    if np.max(heatmap) > 0:
        heatmap /= np.max(heatmap)

    return heatmap


def generate_gradcam(image_path, model_name):

    model = get_model(model_name)

    img_size = MODELS[model_name]["size"]

    layer_name = MODELS[model_name]["layer"]

    img = cv2.imread(
        image_path,
        cv2.IMREAD_GRAYSCALE
    )

    img = cv2.resize(
        img,
        img_size
    )

    if model_name == "custom_cnn":

        input_img = img.astype(np.float32) / 255.0

        input_img = np.expand_dims(
            input_img,
            axis=-1
        )

        input_img = np.expand_dims(
            input_img,
            axis=0
        )

    else:

        rgb_img = cv2.cvtColor(
            img,
            cv2.COLOR_GRAY2RGB
        )

        input_img = np.expand_dims(
            rgb_img.astype(np.float32),
            axis=0
        )

        input_img = preprocess_input(
            input_img
        )

    heatmap = get_heatmap(
        input_img,
        model,
        layer_name
    )

    heatmap = cv2.resize(
        heatmap,
        (img.shape[1], img.shape[0])
    )

    heatmap = np.uint8(
        255 * heatmap
    )

    heatmap_color = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    original_bgr = cv2.cvtColor(
        img,
        cv2.COLOR_GRAY2BGR
    )

    overlay = cv2.addWeighted(
        original_bgr,
        0.6,
        heatmap_color,
        0.4,
        0
    )

    os.makedirs(
        "static/gradcam",
        exist_ok=True
    )

    filename = os.path.basename(
        image_path
    )

    output_path = os.path.join(
        "static/gradcam",
        filename
    )

    cv2.imwrite(
        output_path,
        overlay
    )

    return "/" + output_path.replace(
        "\\",
        "/"
    )