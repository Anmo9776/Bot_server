from flask import Flask, request, jsonify
from transformers import pipeline
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

memory = []

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    memory.append(user_input)
    response = chatbot(user_input, max_length=100)[0]['generated_text']

    memory.append(response)
    return jsonify({"response": response})

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get("message", "")

    if not text:
        return jsonify({"error": "No message provided"}), 400

    tts = gTTS(text)
    tts.save("response.mp3")
    return jsonify({"audio": "response.mp3"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
