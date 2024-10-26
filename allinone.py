import os
from scenedetect import detect, ContentDetector, split_video_ffmpeg
from datetime import timedelta

def detect_and_split_scenes(video_path, threshold=20.0, min_scene_len=25):
    print(f"Processing video: {video_path}")
    print(f"Parameters: threshold={threshold}, min_scene_len={min_scene_len}")

    # Create output directory
    output_dir = 'scenes'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Detect scenes using the new API
        scenes = detect(video_path, ContentDetector(
            threshold=threshold,
            min_scene_len=min_scene_len,
        ))

        print(f"\nDetected {len(scenes)} scenes.")

        if not scenes:
            print("\nNo scenes were detected. Trying with more sensitive parameters...")
            # Retry with more sensitive parameters
            scenes = detect(video_path, ContentDetector(
                threshold=15.0,  # Lower threshold
                min_scene_len=10,  # Shorter minimum scene length
            ))
            print(f"Second attempt detected {len(scenes)} scenes.")

        if scenes:
            # Split the video into scenes
            split_video_ffmpeg(
                video_path,
                scenes,
                output_dir=output_dir,
                show_progress=True
            )

            # Print scene information
            print("\nScene breakdown:")
            for i, scene in enumerate(scenes):
                start_time = scene[0].get_seconds()
                end_time = scene[1].get_seconds()
                duration = end_time - start_time
                print(f"Scene {i+1}: {timedelta(seconds=int(start_time))} - {timedelta(seconds=int(end_time))} (Duration: {timedelta(seconds=int(duration))})")

            print(f"\nScenes have been saved to: {os.path.abspath(output_dir)}")
        else:
            print("\nDetecting and Splitting Failed !!")

    except Exception as e:
        print(f"Error processing video: {str(e)}")
        return None

    return scenes

# Example usage with different sensitivity levels
video_file = "./movie.mp4"  # Replace with your video path

# Try multiple threshold values
thresholds = [40.0, 30.0, 20.0]  # From less to more sensitive

for threshold in thresholds:
  print(f"\nAttempting detection with threshold: {threshold}")
  scenes = detect_and_split_scenes(
      video_file,
      threshold=threshold,
      min_scene_len=25
  )
  if scenes and len(scenes) > 0:
    break






from moviepy.editor import VideoFileClip
import os

def extract_audio(video_path, output_audio_path="audio"):
   video = VideoFileClip(video_path)
   audio = video.audio
   audio.write_audiofile(output_audio_path, codec='pcm_s16le')
   audio.close()
   video.close()

# Process all videos in scenes folder
scenes_dir = './scenes'
audio_dir = './audio'

# Create audio directory if it doesn't exist
os.makedirs(audio_dir, exist_ok=True)

# Iterate through all video files
for video_file in os.listdir(scenes_dir):
  if video_file.endswith(('.mp4')):  # Add more formats if needed
    video_path = os.path.join(scenes_dir, video_file)
    audio_path = os.path.join(audio_dir, os.path.splitext(video_file)[0] + '.wav')
    extract_audio(video_path, audio_path)







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







import json
import google.generativeai as genai
from moviepy.editor import VideoFileClip, concatenate_videoclips
from config import apikey

# Configure the Generative AI model
genai.configure(api_key=apikey)  # Replace with your actual API key

# Generation config (adjust based on API requirements)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="tunedModels/dataset-zk69ms23rjk1",
    generation_config=generation_config,
)

def classify_text(text):
    # Start a chat session to classify the text
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(text)
    return response.text.strip()

def process_text_files(directory='./audio'):
    genre_mapping = {}

    # Loop through all .txt files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            text_file_path = os.path.join(directory, filename)

            # Read the content of the text file
            with open(text_file_path, 'r') as file:
                text_content = file.read()
                
            # Default genre for empty files
            if text_content == "":
                genre_mapping[filename] = "Action"
                continue

            # Classify the text and get the genre
            genre = classify_text(text_content)
            genre_mapping[filename] = genre
            print(f"Classified '{filename}' as genre: {genre}")

    # Save the mapping to a JSON file
    json_file_path = os.path.join(directory, 'genre_mapping.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(genre_mapping, json_file, indent=4)

    print(f"Genre mapping saved to: {json_file_path}")
    return genre_mapping

def load_genre_mappings(genre_mapping_path='./audio/genre_mapping.json'):
    # Load the JSON file containing genre mappings for each clip
    with open(genre_mapping_path, 'r') as json_file:
        return json.load(json_file)

def merge_clips_by_genre(video_directory='./audio', output_directory='./merged_clips'):
    # Load or generate genre mappings
    if not os.path.exists('./audio/genre_mapping.json'):
        genre_mapping = process_text_files(video_directory)
    else:
        genre_mapping = load_genre_mappings()
    
    # Dictionary to store clips by genre
    genre_clips = {}

    # Group clips by genre
    for filename, genre in genre_mapping.items():
        if genre not in genre_clips:
            genre_clips[genre] = []
        video_file_path = os.path.join(video_directory, filename.replace('.txt', '.mp4'))  # Assuming video files are in .mp4
        if os.path.exists(video_file_path):
            genre_clips[genre].append(video_file_path)
        else:
            print(f"Warning: Video file not found for {filename}")

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Merge clips and save into genre-based folders
    for genre, files in genre_clips.items():
        if files:
            clips = [VideoFileClip(file) for file in files]
            merged_clip = concatenate_videoclips(clips, method="compose")
            merged_clip_path = os.path.join(output_directory, f"{genre}.mp4")
            merged_clip.write_videofile(merged_clip_path, codec="libx264")
            print(f"Merged clips for genre '{genre}' saved at: {merged_clip_path}")

# Run the full process
process_text_files()  # Classify text files
merge_clips_by_genre()  # Merge clips by genre

