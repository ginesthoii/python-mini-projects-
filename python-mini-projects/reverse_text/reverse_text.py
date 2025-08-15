def reverse_text(s: str) -> str:
    return s[::-1]

if __name__ == "__main__":
    text = input("Enter text: ")
    print("Reversed:", reverse_text(text))
