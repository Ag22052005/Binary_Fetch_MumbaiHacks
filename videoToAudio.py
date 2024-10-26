# from moviepy.editor import VideoFileClip

# def extract_audio(video_path, output_audio_path):
#     # Load the video file
#     video = VideoFileClip(video_path)
    
#     # Extract the audio from the video
#     audio = video.audio
    
#     # Write the audio to an output file
#     audio.write_audiofile(output_audio_path, codec='pcm_s16le')  # Use .wav or .mp3 extension as needed
    
#     # Close the video and audio clips to release resources
#     audio.close()
#     video.close()

# # Usage
# video_path = './dhruvclips/clip_2.mp4'  # Path to the video file
# output_audio_path = './audio/clip_2.wav'  # .wav or .mp3
# extract_audio(video_path, output_audio_path)









from moviepy.editor import VideoFileClip
import os

def extract_audio(video_path, output_audio_path="audio"):
   video = VideoFileClip(video_path)
   audio = video.audio
   audio.write_audiofile(output_audio_path, codec='pcm_s16le')
   audio.close()
   video.close()

if __name__ == '__main__':
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