# 5-Minute Python Projects — Set 2

More tiny, self-contained Python scripts perfect for quick practice or demos.

## Projects
- **number_guess/** — Number guessing game (1–50).
- **currency_converter/** — USD to EUR/GBP/JPY using static sample rates.
- **file_organizer/** — Sorts files into subfolders by extension.
- **qr_generator/** — Creates a QR code PNG from text/URL. *(needs `qrcode`)*
- **todo_json/** — Minimal to-do list using JSON storage.
- **stopwatch/** — Basic stopwatch with Enter to start/stop.
- **word_frequency/** — Counts words with `collections.Counter`.

## Quick Start (VS Code)
1. Install Python 3.10+ and the VS Code Python extension.
2. Clone this repo and open it in VS Code.
3. (Optional) Create a virtual env:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Run any script from its folder:
   ```bash
   python <scriptname>.py
   ```

## Repo Layout
```
python-mini-projects-2/
├─ number_guess/
│  ├─ number_guess.py
│  └─ README.md
├─ currency_converter/
│  ├─ currency_converter.py
│  └─ README.md
├─ file_organizer/
│  ├─ file_organizer.py
│  └─ README.md
├─ qr_generator/
│  ├─ qr_generator.py
│  └─ README.md
├─ todo_json/
│  ├─ todo_json.py
│  └─ README.md
├─ stopwatch/
│  ├─ stopwatch.py
│  └─ README.md
├─ word_frequency/
│  ├─ word_frequency.py
│  └─ README.md
├─ .gitignore
├─ requirements.txt
├─ LICENSE
└─ README.md
```

## Notes
- For **qr_generator/** you need `qrcode[pil]` (installed via `requirements.txt`).
- All scripts are stdlib-only except QR.
- PRs welcome for more 5-minute ideas!
