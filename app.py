from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import os
from google.cloud import speech

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Konfiguracja klienta Google Speech-to-Text
client = speech.SpeechClient()

# Funkcja do rozpoznawania mowy
def recognize_speech(audio_data):
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="pl-PL"
    )

    response = client.recognize(config=config, audio=audio)
    
    if response.results:
        return response.results[0].alternatives[0].transcript
    else:
        return ""

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@socketio.on('message')
def on_message(data):
    print('Received audio data')
    transcript = recognize_speech(data)
    socketio.emit('message', {'text': transcript})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
