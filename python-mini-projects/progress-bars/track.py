from rich.progress import track
import time

for step in track(range(100), description="Downloading..."):
    time.sleep(0.05)