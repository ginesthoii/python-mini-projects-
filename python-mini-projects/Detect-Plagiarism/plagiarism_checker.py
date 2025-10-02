# Minimal, neutral UI; sensible defaults.

import re
from collections import Counter
from tkinter import Tk, StringVar, BooleanVar, ttk, filedialog

# --- thresholds (percent) ---
LOW_MAX = 30
MID_MAX = 60

# --- verdict colors ---
RED    = "#d9534f"
YELLOW = "#f0ad4e"
GREEN  = "#5cb85c"
NEUTRAL= "#6c757d"

STOPWORDS = set("""
a an the and or but if while to of in on for with at by from up down out over under
this that these those is are was were be been being do does did have has had it as
you your yours he she they them we us our i me my mine not no yes
""".split())

def tokenize(text, drop_stop=False):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if (t not in STOPWORDS)] if drop_stop else tokens

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""

def dice_similarity(t1, t2):
    c1, c2 = Counter(t1), Counter(t2)
    if not c1 and not c2:
        return 0.0, 0
    overlap = sum(min(c1[w], c2[w]) for w in c1.keys() | c2.keys())
    total = sum(c1.values()) + sum(c2.values())
    return (2.0 * overlap) / total, overlap

def jaccard_similarity(t1, t2):
    s1, s2 = set(t1), set(t2)
    if not s1 and not s2:
        return 0.0, 0
    inter = len(s1 & s2)
    union = len(s1 | s2)
    return inter / union, inter

def verdict_and_color(pct):
    if pct <= LOW_MAX: return "Low overlap", GREEN
    if pct <= MID_MAX: return "Moderate overlap", YELLOW
    return "High overlap", RED

def top_overlap_words(t1, t2, k=8):
    c1, c2 = Counter(t1), Counter(t2)
    pairs = [(w, min(c1[w], c2[w])) for w in (c1.keys() | c2.keys())]
    pairs = [(w, n) for w, n in pairs if n > 0]
    pairs.sort(key=lambda x: (-x[1], x[0]))
    return pairs[:k]

class App:
    def __init__(self, root):
        root.title("Text Overlap Checker")
        root.geometry("720x420")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        self.file1 = StringVar(value="(pick File A)")
        self.file2 = StringVar(value="(pick File B)")
        self.metric = StringVar(value="dice")
        self.drop_stop = BooleanVar(value=True)

        main = ttk.Frame(root, padding=16); main.pack(fill="both", expand=True)

        # File pickers
        r1 = ttk.Frame(main); r1.pack(fill="x", pady=(0,8))
        ttk.Label(r1, text="File A:").pack(side="left")
        ttk.Label(r1, textvariable=self.file1).pack(side="left", padx=8)
        ttk.Button(r1, text="Browse…", command=self.pick1).pack(side="right")

        r2 = ttk.Frame(main); r2.pack(fill="x", pady=(0,12))
        ttk.Label(r2, text="File B:").pack(side="left")
        ttk.Label(r2, textvariable=self.file2).pack(side="left", padx=8)
        ttk.Button(r2, text="Browse…", command=self.pick2).pack(side="right")

        # Options
        r3 = ttk.Frame(main); r3.pack(fill="x", pady=(0,8))
        ttk.Label(r3, text="Metric:").pack(side="left", padx=(0,8))
        ttk.Radiobutton(r3, text="Dice (counts matter)", variable=self.metric, value="dice").pack(side="left")
        ttk.Radiobutton(r3, text="Jaccard (unique words)", variable=self.metric, value="jaccard").pack(side="left", padx=(8,0))
        ttk.Checkbutton(r3, text="Remove common stopwords", variable=self.drop_stop).pack(side="right")

        # Result
        self.colorbar = ttk.Frame(main); self.colorbar.pack(fill="x", pady=(8,6))
        self.set_bar_color(NEUTRAL, height=6)

        r4 = ttk.Frame(main); r4.pack(fill="x", pady=(0,6))
        self.percent_var = StringVar(value="–%")
        self.assess_var = StringVar(value="Pick two files and Run")
        ttk.Label(r4, textvariable=self.percent_var, font=("Helvetica", 24, "bold")).pack(side="left")
        ttk.Label(r4, textvariable=self.assess_var).pack(side="left", padx=12)

        # Top words
        ttk.Label(main, text="Top overlapping tokens:").pack(anchor="w", pady=(8,2))
        self.words_box = ttk.Label(main, text="—", wraplength=680, justify="left")
        self.words_box.pack(anchor="w")

        # Run
        r5 = ttk.Frame(main); r5.pack(fill="x", pady=10)
        ttk.Button(r5, text="Run", command=self.run).pack(side="right")

    def set_bar_color(self, color, height=6):
        # Simple color bar using a style on a tiny frame
        s = ttk.Style()
        s.configure("Bar.TFrame", background=color)
        self.colorbar.configure(style="Bar.TFrame")
        self.colorbar["height"] = height

    def pick1(self):
        p = filedialog.askopenfilename(title="Choose File A")
        if p: self.file1.set(p)

    def pick2(self):
        p = filedialog.askopenfilename(title="Choose File B")
        if p: self.file2.set(p)

    def run(self):
        t1 = tokenize(read_file(self.file1.get()), self.drop_stop.get())
        t2 = tokenize(read_file(self.file2.get()), self.drop_stop.get())

        if self.metric.get() == "dice":
            sim, overlap = dice_similarity(t1, t2)
        else:
            sim, overlap = jaccard_similarity(t1, t2)

        pct = int(round(sim * 100))
        verdict, color = verdict_and_color(pct)

        self.percent_var.set(f"{pct}%")
        self.assess_var.set(f"{verdict} • overlap={overlap}")
        self.set_bar_color(color)

        tops = top_overlap_words(t1, t2, k=10)
        self.words_box.configure(
            text=", ".join(f"{w}×{n}" for w, n in tops) if tops else "(no overlapping tokens)"
        )

if __name__ == "__main__":
    root = Tk()
    App(root)
    root.mainloop()