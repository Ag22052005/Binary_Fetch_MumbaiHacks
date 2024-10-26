# import os
# import speech_recognition as sr
# from pydub import AudioSegment

# def audio_to_text(audio_path):
#     print(f"Attempting to load audio file: {audio_path}")
    
#     # Initialize the recognizer
#     recognizer = sr.Recognizer()

#     # Check if the audio file exists
#     if not os.path.exists(audio_path):
#         print(f"Audio file does not exist: {audio_path}")
#         return

#     # Load the audio file
#     try:
#         audio = AudioSegment.from_wav(audio_path)  # Load audio with pydub
#         print("Audio file loaded successfully.")
#     except Exception as e:
#         print(f"Error loading audio file: {e}")
#         return

#     # Process audio in segments
#     segment_length = 60 * 1000  # 1 minute segments
#     total_length = len(audio)
#     transcribed_text = ""

#     for i in range(0, total_length, segment_length):
#         segment = audio[i:i + segment_length]
#         segment_path = f'./audio/segment_{i // segment_length}.wav'
#         segment.export(segment_path, format="wav")  # Save segment as wav file

#         # Recognize the speech in the audio segment
#         with sr.AudioFile(segment_path) as source:
#             audio_data = recognizer.record(source)

#         try:
#             print(f"Attempting to recognize speech in segment {i // segment_length}...")
#             text = recognizer.recognize_google(audio_data)  # Use Google Web Speech API
#             transcribed_text += text + " "
#             print(f"Transcribed Text for segment {i // segment_length}: {text}")
#         except sr.UnknownValueError:
#             print(f"Speech Recognition could not understand audio segment {i // segment_length}.")
#         except sr.RequestError as e:
#             print(f"Could not request results from Google Speech Recognition service; {e}")

#     # Save the transcribed text to a file
#     base_name = os.path.splitext(os.path.basename(audio_path))[0]  # Get the base name without extension
#     text_file_path = f'./audio/{base_name}_transcription.txt'  # Create the text file name
#     with open(text_file_path, 'w') as text_file:
#         text_file.write(transcribed_text.strip())  # Write the transcription to the text file

#     print(f"Complete Transcription saved to: {text_file_path}")

# # Usage
# audio_path = './audio/clip_2.wav'  # Make sure this is the correct path to your audio file
# audio_to_text(audio_path)

import os
import speech_recognition as sr
from pydub import AudioSegment

def audio_to_text(audio_path):
    print(f"Attempting to load audio file: {audio_path}")
    
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Check if the audio file exists
    if not os.path.exists(audio_path):
        print(f"Audio file does not exist: {audio_path}")
        return

    # Load the audio file
    try:
        audio = AudioSegment.from_wav(audio_path)  # Load audio with pydub
        print("Audio file loaded successfully.")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return

    # Process audio in segments
    segment_length = 60 * 1000  # 1 minute segments
    total_length = len(audio)
    transcribed_text = ""

    for i in range(0, total_length, segment_length):
        segment = audio[i:i + segment_length]
        segment_path = f'./audio/segment_{i // segment_length}.wav'
        segment.export(segment_path, format="wav")  # Save segment as wav file

        # Recognize the speech in the audio segment
        with sr.AudioFile(segment_path) as source:
            audio_data = recognizer.record(source)

        try:
            print(f"Attempting to recognize speech in segment {i // segment_length}...")
            text = recognizer.recognize_google(audio_data)  # Use Google Web Speech API
            transcribed_text += text + " "
            print(f"Transcribed Text for segment {i // segment_length}: {text}")
        except sr.UnknownValueError:
            print(f"Speech Recognition could not understand audio segment {i // segment_length}.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    # Save the transcribed text to a file
    base_name = os.path.splitext(os.path.basename(audio_path))[0]  # Get the base name without extension
    text_file_path = f'./audio/{base_name}.txt'  # Create the text file name
    with open(text_file_path, 'w') as text_file:
        text_file.write(transcribed_text.strip())  # Write the transcription to the text file

    print(f"Complete Transcription saved to: {text_file_path}")

def process_all_audio_files(directory='./audio'):
    # Loop through all .wav files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            audio_path = os.path.join(directory, filename)
            audio_to_text(audio_path)

# Usage
process_all_audio_files()  # Process all audio files in the './audio' directory
