from flask import Flask, render_template, request, redirect
from PIL import Image
import os

from backend.report_generator import generate_report
from backend.predictor import predict_image
from backend.gradcam import generate_gradcam

from database import (
    initialize_database,
    save_prediction,
    get_history,
    delete_record,
    search_history,
    get_statistics
)

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# =====================================
# ALLOWED IMAGE TYPES
# =====================================

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg"
}


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


initialize_database()

# =====================================
# FOLDERS
# =====================================

UPLOAD_FOLDER = os.path.join(
    "static",
    "uploads"
)

GRADCAM_FOLDER = os.path.join(
    "static",
    "gradcam"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    GRADCAM_FOLDER,
    exist_ok=True
)

# =====================================
# HOME PAGE
# =====================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# =====================================
# PREDICTION
# =====================================

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:

        return render_template(
            "index.html"
        )

    file = request.files["image"]

    if file.filename == "":

        return render_template(
            "index.html",
            error="Please choose an image."
        )

    if not allowed_file(file.filename):

        return render_template(
            "index.html",
            error="Please upload a valid chest X-ray image (JPG, JPEG or PNG)."
        )

    # -----------------------------
    # Patient Details
    # -----------------------------

    patient_name = request.form["patient_name"]

    age = request.form["age"]

    gender = request.form["gender"]

    model_name = request.form["model"]

    # -----------------------------
    # Display Model Name
    # -----------------------------

    model_display = {

        "tbnet": "TBNet (Recommended)",

        "resnet50": "ResNet50",

        "efficientnetb4": "EfficientNetB4",

        "densenet121": "DenseNet121",

        "custom_cnn": "Custom CNN"

    }.get(model_name, model_name)
        # -----------------------------
    # Save Uploaded Image
    # -----------------------------

    filename = file.filename

    image_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(
        image_path
    )

    # -----------------------------
    # Read Image
    # -----------------------------

    try:

        image = Image.open(
            image_path
        ).convert("L")

    except Exception:

        return render_template(

            "index.html",

            error="The uploaded image could not be read. Please upload a valid chest X-ray."

        )

    # -----------------------------
    # Prediction
    # -----------------------------

    try:

        prediction, confidence = predict_image(

            image,

            model_name

        )

    except Exception as e:

        print("Prediction Error:", e)

        return render_template(

            "index.html",

            error="Prediction failed. Please try another image."

        )

    uploaded_image = "/" + image_path.replace(

        "\\",

        "/"

    )

    # -----------------------------
    # Grad-CAM
    # -----------------------------

    gradcam_image = None
    gradcam_message = None

    if model_name == "custom_cnn":

        gradcam_message = (

            "Grad-CAM visualization is currently unavailable for the selected "
            "Custom CNN model because this architecture is not compatible "
            "with the Grad-CAM implementation used in this system. "
            "Please select TBNet, ResNet50, EfficientNetB4 or DenseNet121 "
            "to generate a Grad-CAM visualization."

        )

    else:

        try:

            gradcam_image = generate_gradcam(

                image_path,

                model_name

            )

        except Exception as e:

            print("Grad-CAM Error:", e)

            gradcam_message = (

                "Unable to generate Grad-CAM."

            )

            gradcam_image = None

    # -----------------------------
    # PDF Report
    # -----------------------------

    pdf_report = generate_report(

        patient_name,

        age,

        gender,

        prediction,

        confidence,

        model_display,

        image_path,

        gradcam_image[1:] if gradcam_image else None

    )

    # -----------------------------
    # Save Prediction
    # -----------------------------

    save_prediction(

        patient_name,

        age,

        gender,

        model_display,

        prediction,

        confidence,

        uploaded_image,

        gradcam_image,

        pdf_report

    )

    # -----------------------------
    # Return Result
    # -----------------------------

    return render_template(

        "index.html",

        patient_name=patient_name,

        age=age,

        gender=gender,

        prediction=prediction,

        confidence=confidence,

        selected_model=model_display,

        uploaded_image=uploaded_image,

        gradcam_image=gradcam_image,

        gradcam_message=gradcam_message,

        pdf_report=pdf_report

    )
    # =====================================
# HISTORY PAGE
# =====================================

@app.route("/history")
def history():

    keyword = request.args.get(

        "search",

        ""

    ).strip()

    if keyword:

        history_records = search_history(

            keyword

        )

    else:

        history_records = get_history()

    stats = get_statistics()

    return render_template(

        "history.html",

        history=history_records,

        stats=stats,

        keyword=keyword

    )


# =====================================
# DELETE RECORD
# =====================================

@app.route("/delete/<int:record_id>")
def delete(record_id):

    delete_record(

        record_id

    )

    return redirect(

        "/history"

    )


# =====================================
# ABOUT PAGE
# =====================================

@app.route("/about")
def about():

    return render_template(

        "about.html"

    )


# =====================================
# CONTACT PAGE
# =====================================

@app.route("/contact")
def contact():

    return render_template(

        "contact.html"

    )


# =====================================
# RUN APPLICATION
# =====================================

if __name__ == "__main__":

    app.run(

        debug=True

    )
    