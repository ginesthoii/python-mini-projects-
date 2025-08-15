from collections import Counter

def count_words(text: str):
    return Counter(text.lower().split())

if __name__ == "__main__":
    text = input("Enter text: ")
    counts = count_words(text)
    for word, count in counts.items():
        print(f"{word}: {count}")
