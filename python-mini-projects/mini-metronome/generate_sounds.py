import math
import wave
import struct
import os

def make_click(path, freq=1000, ms=25, volume=0.5, sample_rate=44100):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    frames = int(sample_rate * (ms / 1000.0))
    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)  # 16-bit
        w.setframerate(sample_rate)
        for i in range(frames):
            t = i / sample_rate
            env = math.exp(-30 * t)  # fast decay
            sample = volume * env * math.sin(2 * math.pi * freq * t)
            val = int(sample * 32767)
            w.writeframes(struct.pack('<h', val))

if __name__ == "__main__":
    make_click(os.path.join("sounds", "click_hi.wav"), freq=1400, ms=22, volume=0.6)
    make_click(os.path.join("sounds", "click_lo.wav"), freq=900,  ms=22, volume=0.55)
    print("Generated sounds/click_hi.wav and sounds/click_lo.wav")