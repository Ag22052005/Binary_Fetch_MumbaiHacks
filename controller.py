import subprocess

subprocess.run(["python", "sceneDetectandSplit.py"])
subprocess.run(["python", "videoToAudio.py"])
subprocess.run(["python", "audioToText.py"])
subprocess.run(["python", "transcriptToGenre.py"])
