from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
import pytesseract
import openai
import os
import tempfile
import time

# Configure OpenAI API key
openai.api_key = 'sk-proj-p68xqKwS8GE2fzb3lWSCT3BlbkFJ66F8AUZJn2RMOQEe2DGU'

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='fra')
        return text
    except (PermissionError, UnidentifiedImageError):
        raise Exception(f"Cannot process image file: {image_path}")

def ask_openai(extracted_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"répondre aux questions en se basant sur les choix donnés sans donner des explications : {extracted_text}"
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if response.choices:
        choice = response.choices[0]
        if 'message' in choice and 'content' in choice.message:
            return choice.message['content']
    return "No response from OpenAI"

def generate_response(extracted_text):
    first_response = ask_openai(extracted_text)
    time.sleep(1)  # Adding a short delay to mimic asking the question again
    second_response = ask_openai(extracted_text)
    
    if first_response == second_response:
        return first_response
    else:
        time.sleep(1)  # Adding a short delay before asking the third time
        third_response = ask_openai(extracted_text)
        return third_response

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            extracted_text = extract_text_from_image(temp_file.name)
            response = generate_response(extracted_text)
            return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(temp_file.name)

if __name__ == '__main__':
    app.run(debug=True)
