# 🫁 TB-AI Detection System

An AI-powered web application for automated detection of pulmonary tuberculosis from chest X-ray images using deep learning.

This project was developed as a Final Year Project (FYP) for the Department of Computer Science.



## Features

- Automated Tuberculosis Detection
- Five Deep Learning Models
  - TBNet (Proposed)
  - ResNet50V2
  - DenseNet121
  - EfficientNetB4
  - Custom CNN
- Explainable AI using Grad-CAM
- Patient Information Management
- Prediction History (SQLite)
- Search Prediction History
- PDF Report Generation
- Professional Web Interface (Flask)


## Technology Stack

- Python
- Flask
- TensorFlow / Keras
- OpenCV
- Pillow
- SQLite
- ReportLab
- HTML
- CSS
- JavaScript


## Project Structure

deployment/
│
├── backend/
├── models/
├── static/
├── templates/
├── app.py
├── database.py
├── requirements.txt
└── README.md




## Installation

Clone the repository
bash
git clone https://github.com/USERNAME/TB-AI-Detection-System.git


Go into the project
bash
cd deployment


Create a virtual environment

bash
python -m venv venv


Activate it

Windows

bash
venv\Scripts\activate


Install dependencies

bash
pip install -r requirements.txt


Run the application

bash
python app.py

## Trained Models

The trained deep learning models are not included in this repository because they exceed GitHub's file size limit.

Download the models from:

**https://drive.google.com/drive/folders/1c7sJhtEi0wtUPFW6KmITYjCwJP7fu4M2?usp=sharing**

After downloading, place the model files inside the `models/` folder before running the application.

## Dataset

The dataset used for training consists of Chest X-ray images of:

- Tuberculosis
- Normal

Images were resized and preprocessed before training.

---

## Proposed Model

The proposed **TBNet** model achieved the highest performance among all evaluated models.

| Model | Accuracy |
|--------|-----------|
| TBNet | **97.50%** |
| ResNet50V2 | 96.83% |
| EfficientNetB4 | 96.16% |
| DenseNet121 | 95.50% |
| Custom CNN | 95.00% |

---

## Disclaimer

This application is intended for educational and research purposes only.

It should not be used as a substitute for professional medical diagnosis.

---

## Authors

Muhammad Umar Shamas Nasir

Muhammad Bilal

Department of Computer Science

University of Engineering and Technology (UET) Peshawar