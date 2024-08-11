import base64
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
from PIL import Image
import io

# Load the trained model
model = tf.keras.models.load_model('digit_recognition_model.h5')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image data from the POST request
        data = request.get_json()
        image_data = data['image']
        
        # Decode the base64 image
        image = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image)).convert('L')  # Convert to grayscale
        
        # Resize and reshape the image to match the model's input shape
        image = image.resize((28, 28))
        image = np.array(image, dtype=np.float32).reshape((28, 28, 1)) / 255.0
        image = np.expand_dims(image, axis=0)
        
        # Debug: Check the shape of the image and its content
        print("Image shape:", image.shape)
        print("Image data:", image)
        
        # Make a prediction
        prediction = model.predict(image)
        
        # Debug: Check the prediction output
        print("Model prediction:", prediction)
        
        digit = np.argmax(prediction)
        
        return jsonify({'digit': int(digit)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
