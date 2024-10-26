import os
import speech_recognition as sr

def audio_to_text(audio_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file

    # Recognize the speech in the audio file
    try:
        text = recognizer.recognize_google(audio_data)  # Use Google Web Speech API
        print("Transcribed Text:")
        print(text)
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Usage
audio_path = './audio/audio.wav'  # Make sure this is the correct path to your audio file
audio_to_text(audio_path)
