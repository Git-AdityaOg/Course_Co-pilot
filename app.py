# app.py
from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import openai
import speech_recognition as sr
import requests

# Initialize Flask app
app = Flask(__name__)

# OpenAI API Key
openai.api_key = "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"

# Initialize Google Translator
translator = Translator()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for content translation
@app.route('/translate', methods=['POST'])
def translate_content():
    content = request.form['content']
    target_lang = request.form['target_lang']
    translated = translator.translate(content, dest=target_lang)
    return jsonify({'translated_content': translated.text})

# Route for text-to-speech conversion
@app.route('/voiceover', methods=['POST'])
def generate_voiceover():
    content = request.form['content']
    lang = request.form['lang']
    tts = gTTS(text=content, lang=lang)
    tts.save("static/voiceover.mp3")
    return jsonify({'audio_file': 'static/voiceover.mp3'})

# Route for speech-to-text conversion
@app.route('/stt', methods=['POST'])
def audio_to_text():
    file = request.files['audio']
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file)
    with audio_file as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return jsonify({'lecture_notes': text})

# Route for content suggestions
@app.route('/suggest_content', methods=['POST'])
def suggest_content():
    topic = request.form['topic']
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"Suggest topics and resources for the course on {topic}.",
      max_tokens=100
    )
    suggestions = response['choices'][0]['text']
    return jsonify({'suggestions': suggestions})

# Route for image suggestions using Unsplash API
@app.route('/suggest_images', methods=['POST'])
def suggest_images():
    topic = request.form['topic']
    api_url = f"https://api.unsplash.com/search/photos?query={topic}&client_id=sAOlwQ5zhi_vaXdXTHKRc9ksI_eYth7CAQW1rM3tPME"
    response = requests.get(api_url)
    images = response.json().get('results', [])
    image_urls = [image['urls']['small'] for image in images]
    return jsonify({'images': image_urls[:5]})

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
