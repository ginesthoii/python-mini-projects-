
# python-mini-projects

Tiny, self-contained Python scripts that I built for practice, experiments, and fun.
Each project lives in its own folder and runs with a single command in the terminal.

Think of this repo as my Python sketchbook — quick ideas, simple tools, and little demos that helped me learn by building.

---

## What’s Inside
- password_generator/ — Create random, secure passwords using letters, digits, and punctuation.
- countdown/ — A simple countdown timer (powered by time.sleep).
- dice/ — Roll a six-sided die.
- reverse_text/ — Flip any string backwards instantly.
- weather/ — Minimal OpenWeather client (requires an API key).
- number_guess/ — Classic guessing game (pick a number between 1–50).
- currency_converter/ — Quick USD → EUR/GBP/JPY converter with static sample rates.
- file_organizer/ — Sort messy folders by file extension.
- qr_generator/ — Turn text/URLs into QR codes (needs qrcode[pil]).
- todo_json/ — Minimal to-do list using JSON storage.
- stopwatch/ — Start/stop timer with the Enter key.
- word_frequency/ — Count word frequencies with collections.Counter.
- mini-metronome/ — A command-line metronome with accented downbeats (using afplay on macOS or simpleaudio elsewhere).

---

## Notes
- For `qr_generator/` you need `qrcode[pil]` (installed via `requirements.txt`).
- All scripts are stdlib-only except QR and Weather (`requests`)
