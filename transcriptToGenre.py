# import requests

# def get_genre(prompt):
#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyDe9wzFrqaJ2HJTZ9UuDoXTEKbxjd5OVqA"  # Replace with your actual API key
#     headers = {
#         "Content-Type": "application/json",
#     }
    
#     # The data structure should align with the API requirements
#     data = {
#         "contents": [
#             {
#                 "parts": [
#                     {
#                         "text": f"What is the genre of the following text, answer in one word only that is the genre. never answer no genre found , answer in that case with action, comedy, thriller , drama, horror ,love: '{prompt}'?"
#                     }
#                 ]
#             }
#         ]
#     }

#     try:
#         # Make the request to the Gemini API
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()  # Raise an error for bad responses

#         # Extract and return the genre from the response
#         genre = response.json().get("contents", [{}])[0].get("parts", [{}])[0].get("text", "No genre found.")
#         return genre.strip()  # Clean up the output
#     except requests.exceptions.HTTPError as http_err:
#         return f"HTTP error occurred: {http_err}"
#     except Exception as err:
#         return f"An error occurred: {err}"

# def read_text_file(file_path):
#     """Reads the text from the specified file and returns it."""
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             text = file.read()
#         return text
#     except Exception as e:
#         return f"An error occurred while reading the file: {e}"

# if __name__ == "__main__":
#     # Path to the text file containing the extracted audio transcription
#     text_file_path = './audio/clip_2_transcription.txt'  # Update with your text file path
#     extracted_text = read_text_file(text_file_path)
    
#     if "error" in extracted_text.lower():
#         print(extracted_text)  # Print any errors in reading the file
#     else:
#         genre = get_genre(extracted_text)
#         print(f"Extracted Text: {extracted_text}")
#         print(f"Detected Genre: {genre}")





import os
import json
import google.generativeai as genai
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Configure the Generative AI model
genai.configure(api_key="AIzaSyDe9wzFrqaJ2HJTZ9UuDoXTEKbxjd5OVqA")  # Replace with your actual API key

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
if __name__ == "__main__":
    process_text_files()  # Classify text files
    merge_clips_by_genre()  # Merge clips by genre

