from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# ----------------------------
# Load trained model
# ----------------------------
# MODEL_PATH = "leaf_disease_model.h5"  # or your .h5 model
MODEL_PATH = "leaf_disease_mobilenet.h5"  # or your .h5 model
model = load_model(MODEL_PATH)

# ----------------------------
# Classes (must match training)
# ----------------------------
classes = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

# ----------------------------
# Home route
# ----------------------------
@app.route('/')
def home():
    return render_template("index.html")


# ----------------------------
# Prediction route
# ----------------------------
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    # Save uploaded file temporarily
    filepath = os.path.join("static", file.filename)
    file.save(filepath)

    # Preprocess image
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Prediction
    preds = model.predict(img_array)
    predicted_index = np.argmax(preds)
    predicted_class = classes[predicted_index]
    confidence = round(float(preds[0][predicted_index]) * 100, 2)

    # Render only top prediction and confidence
    return render_template(
        "index.html",
        prediction=predicted_class,
        confidence=confidence
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
