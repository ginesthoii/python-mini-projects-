import random

def roll_dice(sides=6):
    return random.randint(1, sides)

if __name__ == "__main__":
    print(f"You rolled a {roll_dice()}")
