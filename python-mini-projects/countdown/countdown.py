import time

def countdown(seconds: int):
    for i in range(seconds, 0, -1):
        print(i)
        time.sleep(1)
    print("Time's up!")

if __name__ == "__main__":
    seconds = int(input("Enter countdown time in seconds: "))
    countdown(seconds)
