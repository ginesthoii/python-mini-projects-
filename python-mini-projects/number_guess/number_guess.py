import random

def play():
    secret = random.randint(1, 50)
    tries = 0
    print("Guess my number (1–50)!")
    while True:
        guess = input("Your guess: ")
        if not guess.isdigit():
            print("Enter a number.")
            continue
        guess = int(guess)
        tries += 1
        if guess == secret:
            print(f"Correct! You got it in {tries} tries.")
            break
        elif guess < secret:
            print("Too low!")
        else:
            print("Too high!")

if __name__ == "__main__":
    play()
