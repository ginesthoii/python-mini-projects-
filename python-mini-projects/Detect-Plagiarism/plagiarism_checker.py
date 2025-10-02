# plagiarism_checker.py
import re
from tkinter import Tk, Label

def tokenize(path):
    """Return a list of lowercase alphanumeric tokens from a text file."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().lower()
    # Grab alphanumeric word chunks like "hello", "python3"
    return re.findall(r"[a-z0-9]+", text)

def dice_similarity(tokens1, tokens2):
    """
    Sørensen–Dice coefficient using multiset overlap.
    2 * sum(min(count1[w], count2[w])) / (len1 + len2)
    """
    from collections import Counter
    c1, c2 = Counter(tokens1), Counter(tokens2)
    overlap = sum(min(c1[w], c2[w]) for w in c1.keys() | c2.keys())
    total = sum(c1.values()) + sum(c2.values())
    if total == 0:
        return 0.0
    return (2.0 * overlap) / total

def main(file1="File_1.txt", file2="File_2.txt"):
    l1 = tokenize(file1)
    l2 = tokenize(file2)

    percent = round(dice_similarity(l1, l2) * 100)

    # Pick color by threshold
    if percent <= 30:
        bg = "Green"
    elif percent <= 60:
        bg = "Yellow"
    else:
        bg = "Red"

    result = f"The Plagiarized Content Percent between the two files is {percent}%"

    # Simple Tkinter window with a label
    win = Tk()
    win.title("Plagiarism Checker")
    win.geometry("800x200")
    label = Label(win, text=result, bg=bg, fg="black", font=("Helvetica", 16, "bold"))
    label.pack(expand=True, fill="both")
    win.mainloop()

if __name__ == "__main__":
    main()