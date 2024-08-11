import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request

# Load the trained model
model = tf.keras.models.load_model('digit_recognition_model.h5')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the image data from the POST request
    image = request.form['image']  # image data from canvas
    
    # Preprocess the image to match the model's input shape
    image = np.array(image, dtype=np.float32).reshape((28, 28, 1)) / 255.0
    image = np.expand_dims(image, axis=0)

    # Make a prediction
    prediction = model.predict(image)
    digit = np.argmax(prediction)
    
    return str(digit)

if __name__ == '__main__':
    app.run(debug=True)
