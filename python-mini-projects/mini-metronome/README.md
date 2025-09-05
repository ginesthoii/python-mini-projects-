# Mini Metronome (CLI)

Self-contained Python metronome. No deps required for text mode; optional audio clicks via `simpleaudio`.

## Run

```bash
# text mode (no deps)
python metronome.py 100 -n 16 -m 4/4

# audio mode
pip install -r requirements.txt
python generate_sounds.py
python metronome.py 100 -n 16 -m 4/4