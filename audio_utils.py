# audio_utils.py
import threading
import os
import time
import pygame

pygame.mixer.init()

dir_path = os.path.dirname(__file__)

def play_sound(filename: str) -> None:
    """
    Memutar file suara (MP3 atau WAV) secara non-blocking menggunakan pygame.

    :param filename: Nama file suara termasuk ekstensi (.mp3 atau .wav).
    """
    sound_path = os.path.join(dir_path, "assets", filename)  # <-- Perubahan di sini
    if not os.path.isfile(sound_path):
        print(f"Warning: Sound file not found: {sound_path}")
        return

    def _play():
        try:
            sound = pygame.mixer.Sound(sound_path)
            channel = sound.play()
            while channel.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"Error playing sound {sound_path}: {e}")

    threading.Thread(target=_play, daemon=True).start()

def play_sound_effect(is_correct: bool) -> None:
    """
    Memutar efek suara berdasarkan kondisi benar atau salah.

    :param is_correct: True untuk efek benar (ping), False untuk efek salah (beep)
    """
    filename = "sound_ping.mp3" if is_correct else "sound_beep.mp3"
    play_sound(filename)
