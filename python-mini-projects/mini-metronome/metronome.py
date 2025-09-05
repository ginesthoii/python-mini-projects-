#!/usr/bin/env python3
"""
Mini Python Metronome

- Accurate timing with drift compensation
- Downbeat accent using meter top number (e.g., 4/4, 3/4)
- Sound backends:
    * auto       → on macOS prefers 'afplay', otherwise tries simpleaudio
    * simpleaudio→ non-blocking Python playback (may segfault on some macOS setups)
    * afplay     → uses macOS built-in CLI player (stable)
    * none       → terminal bell only

Usage examples:
    python metronome.py 120 -n 16 -m 4/4
    python metronome.py 90  -n 12 -m 3/4 --backend afplay
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from typing import Optional

# ------------ Config ------------

CLICK_HI = os.path.join("sounds", "click_hi.wav")
CLICK_LO = os.path.join("sounds", "click_lo.wav")
BACKENDS = ("auto", "simpleaudio", "afplay", "none")


# ------------ Backend selection & helpers ------------

def choose_backend(requested: str) -> str:
    """
    Decide which backend to use.
    - If explicitly requested: honor it (fall back to 'none' if unavailable).
    - If auto:
        * On macOS (darwin): prefer 'afplay' if available (most stable).
        * Else: prefer 'simpleaudio' if having an issue with it, use 'afplay' if present.
    """
    if requested == "simpleaudio":
        try:
            import simpleaudio as _sa  # noqa: F401
            return "simpleaudio"
        except Exception:
            return "none"

    if requested == "afplay":
        return "afplay" if shutil.which("afplay") else "none"

    if requested == "none":
        return "none"

    # auto
    if sys.platform == "darwin" and shutil.which("afplay"):
        return "afplay"
    try:
        import simpleaudio as _sa  # noqa: F401
        return "simpleaudio"
    except Exception:
        pass
    if shutil.which("afplay"):
        return "afplay"
    return "none"


_sa = None  # late-bound simpleaudio module


def load_sound_simpleaudio(path: str):
    """Preload WAV as a WaveObject (simpleaudio)."""
    global _sa
    import simpleaudio as sa  # imported lazily so other backends don't require it
    _sa = sa
    return sa.WaveObject.from_wave_file(path)


def play_simpleaudio(wave_obj) -> None:
    try:
        wave_obj.play()  # fire-and-forget
    except Exception:
        pass


def play_afplay(path: str) -> None:
    """Spawn macOS 'afplay' to play a file, non-blocking."""
    try:
        subprocess.Popen(
            ["afplay", path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def bell() -> None:
    sys.stdout.write("\a")
    sys.stdout.flush()


# ------------ Core metronome ------------

def metronome(bpm: int, beats: Optional[int], meter: str, backend: str = "auto") -> None:
    """
    Run a metronome at the given BPM.

    Args:
        bpm: beats per minute (must be > 0)
        beats: total beats to play (None = infinite)
        meter: e.g., '4/4' or '3/4' (only the top number is used for accenting)
        backend: 'auto' | 'simpleaudio' | 'afplay' | 'none'
    """
    # Validate meter & extract top number
    try:
        top = int(meter.split("/")[0])
        if top < 1:
            raise ValueError
    except Exception:
        print(f"Invalid meter '{meter}'. Use like '4/4' or '3/4'.")
        sys.exit(1)

    if bpm <= 0:
        print("BPM must be a positive integer.")
        sys.exit(1)

    mode = choose_backend(backend)
    interval = 60.0 / bpm
    count = 0

    # Prepare click function for chosen backend
    if mode == "simpleaudio":
        hi = load_sound_simpleaudio(CLICK_HI) if os.path.exists(CLICK_HI) else None
        lo = load_sound_simpleaudio(CLICK_LO) if os.path.exists(CLICK_LO) else None

        def play_click(is_downbeat: bool) -> None:
            w = hi if (is_downbeat and hi is not None) else lo
            if w is not None:
                play_simpleaudio(w)
            else:
                bell()

    elif mode == "afplay":

        def play_click(is_downbeat: bool) -> None:
            path = CLICK_HI if is_downbeat else CLICK_LO
            if os.path.exists(path):
                play_afplay(path)
            else:
                bell()

    else:  # 'none'
        def play_click(is_downbeat: bool) -> None:  # noqa: ARG001
            bell()

    print(f"Metronome: {bpm} bpm, meter {meter} (backend: {mode})")
    print("Press Ctrl+C to stop.\n")

    try:
        start = time.perf_counter()
        while True:
            count += 1
            is_downbeat = (count - 1) % top == 0

            # Visual cue
            sys.stdout.write("TICK\n" if is_downbeat else "tick\n")
            sys.stdout.flush()

            # Sound cue
            play_click(is_downbeat)

            # Drift-resistant sleep (schedule next beat relative to start)
            next_beat_time = start + count * interval
            remaining = next_beat_time - time.perf_counter()
            if remaining > 0:
                time.sleep(remaining)

            if beats is not None and count >= beats:
                break

    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"\nError: {e}")


# ------------ CLI ------------

def main() -> None:
    p = argparse.ArgumentParser(description="Mini Python Metronome")
    p.add_argument("bpm", type=int, help="Beats per minute (e.g., 60, 90, 120)")
    p.add_argument("-n", "--beats", type=int, default=None, help="Total beats to play (default: infinite)")
    p.add_argument("-m", "--meter", type=str, default="4/4", help="Meter for accenting (e.g., 4/4, 3/4)")
    p.add_argument(
        "--backend",
        choices=BACKENDS,
        default="auto",
        help="Sound backend: auto | simpleaudio | afplay | none (auto prefers afplay on macOS)",
    )
    args = p.parse_args()

    metronome(args.bpm, args.beats, args.meter, backend=args.backend)


if __name__ == "__main__":
    main()