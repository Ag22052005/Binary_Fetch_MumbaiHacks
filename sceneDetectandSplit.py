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

if __name__ == "__main__":
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


    