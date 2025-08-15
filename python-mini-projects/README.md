# 5‑Minute Python Projects

Tiny, self-contained Python scripts that are perfect for quick practice or demos. Each project lives in its own folder and runs in a terminal with one command.

## Projects
- **password_generator/** — Random password using letters, digits, punctuation.
- **countdown/** — Simple countdown timer using `time.sleep`.
- **dice/** — Six-sided dice roller.
- **reverse_text/** — Reverse any input string.
- **weather/** — Minimal OpenWeather client (needs API key).

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
4. For **weather/**, set your API key (either export env var or add `.env` at project root):
   ```bash
   # .env file at project root
   OPENWEATHER_API_KEY=your_key_here
   ```
5. Run any script from its folder:
   ```bash
   python <scriptname>.py
   ```

## Repo Layout
```
python-mini-projects/
├─ password_generator/
│  ├─ password_generator.py
│  └─ README.md
├─ countdown/
│  ├─ countdown.py
│  └─ README.md
├─ dice/
│  ├─ dice.py
│  └─ README.md
├─ reverse_text/
│  ├─ reverse_text.py
│  └─ README.md
├─ weather/
│  ├─ weather.py
│  └─ README.md
├─ .gitignore
├─ requirements.txt
├─ LICENSE
└─ README.md
```

## Suggested Next Additions
- Unit tests (`pytest`) for tiny functions (e.g., reverser, dice range).
- Add a CLI wrapper with `argparse` for length, sides, etc.
- Package a few as `pipx`-installable utilities.
