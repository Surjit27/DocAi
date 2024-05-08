from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import cv2
import numpy as np
import base64

import os
import uuid
from PIL import Image
from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import pak
import pak.indexmodel  

app = Flask(__name__)

genai.configure(api_key="AIzaSyCI9IPlNmnTGPFVdc_BJnKBa9GC-fnBNrU")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-content', methods=['POST'])
def generate_content():
    data = request.json
    user_input = data['userInput']
    print("User input received from JavaScript:", user_input)

    model = genai.GenerativeModel("models/gemini-pro")  
    response = model.generate_content(user_input)

    generated_content = response.text

    return jsonify({'message': generated_content})

@app.route('/generate-default-text', methods=['POST'])
def generate_default_text():
    model = genai.GenerativeModel("models/gemini-pro")  
    default_text = model.generate_default_text()

    return jsonify({'message': default_text})
UPLOAD_FOLDER = r"C:\Users\S R SURJIT KUMAR\Downloads\website real"

@app.route('/process-image', methods=['POST'])
def process_image():
    image_data = request.files['image']

    if image_data.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = str(uuid.uuid4()) + '.png'  

    image_path = os.path.join(UPLOAD_FOLDER, filename)
    print(image_path)
    
    # Convert and save the image as PNG format
    with Image.open(image_data) as img:
        img.save(image_path, 'PNG')

    
    predictor = pak.indexmodel.ModelPredictor(column="Main", current_index=None, input_file=img)
    prediction_result = predictor.run() 
    model = genai.GenerativeModel("models/gemini-pro")  
    response = model.generate_content(prediction_result)

    generated_content = response.text

    return jsonify({'message': generated_content})


if __name__ == '__main__':
    app.run(debug=True)






