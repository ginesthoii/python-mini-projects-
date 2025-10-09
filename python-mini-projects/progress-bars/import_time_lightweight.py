import time, sys

for i in range(101):
    bar = '█' * (i // 2) + '-' * (50 - i // 2)
    sys.stdout.write(f"\rDownloading |{bar}| {i}%")
    sys.stdout.flush()
    time.sleep(0.05)

print("\nDone!")