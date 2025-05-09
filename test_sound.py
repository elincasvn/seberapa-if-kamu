import subprocess

# Play correct sound using macOS native audio player
subprocess.Popen(["afplay", "assets/sound_correct.mp3"])