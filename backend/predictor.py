import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input

MODELS = {
    "custom_cnn": "models/custom_cnn_best.keras",
    "densenet121": "models/densenet121_best.keras",
    "efficientnetb4": "models/efficientnetb4_best.keras",
    "resnet50": "models/resnet50_v2_best.keras",
    "tbnet": "models/tbnet_best.keras"
}

loaded_models = {}

def get_model(model_name):

    if model_name not in loaded_models:

        print(f"Loading {model_name}...")

        loaded_models[model_name] = load_model(
            MODELS[model_name],
            compile=False
        )

    return loaded_models[model_name]


def predict_image(image, model_name):

    model = get_model(model_name)

    # -------------------------
    # CUSTOM CNN
    # -------------------------

    if model_name == "custom_cnn":

        image = image.resize((256, 256))

        image = np.array(image)

        image = image.astype("float32") / 255.0

        image = np.expand_dims(image, axis=-1)

        image = np.expand_dims(image, axis=0)

    # -------------------------
    # EFFICIENTNETB4
    # -------------------------

    elif model_name == "efficientnetb4":

        image = image.resize((380, 380))

        image = np.array(image)

        if len(image.shape) == 2:
            image = np.stack([image] * 3, axis=-1)

        image = image.astype(np.float32)

        image = preprocess_input(image)

        image = np.expand_dims(image, axis=0)

    # -------------------------
    # DENSENET121
    # RESNET50
    # TBNET
    # -------------------------

    else:

        image = image.resize((256, 256))

        image = np.array(image)

        if len(image.shape) == 2:
            image = np.stack([image] * 3, axis=-1)

        image = image.astype(np.float32)

        image = preprocess_input(image)

        image = np.expand_dims(image, axis=0)

    prediction = model.predict(
        image,
        verbose=0
    )[0][0]

    print(
        f"{model_name} raw prediction = {prediction}"
    )

    if prediction >= 0.5:

        label = "Tuberculosis"

        confidence = prediction * 100

    else:

        label = "Normal"

        confidence = (1 - prediction) * 100

    confidence = float(round(confidence, 2))

    return label, confidence