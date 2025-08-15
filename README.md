
## python-mini-projects

Mini, self-contained Python scripts perfect for quick practice or demos.  
Each project lives in its own folder and runs in a terminal with one command.

## Projects
- **password_generator/** — Random password using letters, digits, punctuation.
- **countdown/** — Simple countdown timer using `time.sleep`.
- **dice/** — Six-sided dice roller.
- **reverse_text/** — Reverse any input string.
- **weather/** — Minimal OpenWeather client (needs API key — see below).  
  Get an API key: https://openweathermap.org/api
- **number_guess/** — Number guessing game (1–50).
- **currency_converter/** — USD → EUR/GBP/JPY using static sample rates.
- **file_organizer/** — Sorts files into subfolders by extension.
- **qr_generator/** — Creates a QR code PNG from text/URL (needs `qrcode[pil]`).
- **todo_json/** — Minimal to-do list using JSON storage.
- **stopwatch/** — Basic stopwatch with Enter to start/stop.
- **word_frequency/** — Counts words with `collections.Counter`.


## Quick Start (VS Code)
1. Install Python 3.10+ and the VS Code Python extension.
2. Clone this repo and open it in VS Code.
3. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. For `weather/`, set your API key (either export env var or add `.env` at project root):
   ```bash
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
- For `qr_generator/` you need `qrcode[pil]` (installed via `requirements.txt`).
- All scripts are stdlib-only except QR and Weather (`requests`)
```


Have fun!
