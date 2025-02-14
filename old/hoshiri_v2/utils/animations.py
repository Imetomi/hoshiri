# hoshiri/utils/animations.py

import time
import sys


def thinking_animation(duration=1.5):
    """
    Displays a short "Thinking..." animation.
    We'll print dots in a loop, overwriting the same line.
    """
    message = "Thinking"
    start_time = time.time()
    dot_sequence = [".", "..", "..."]  # Simple 3-step progression

    i = 0
    while time.time() - start_time < duration:
        # Overwrite the same line with carriage return
        sys.stdout.write(f"\r{message}{dot_sequence[i % len(dot_sequence)]}")
        sys.stdout.flush()
        time.sleep(0.3)
        i += 1

    # Clear the line after finishing
    clear_line(message + "...")


def processing_animation(duration=1.5):
    """
    Displays a short "Processing results..." animation,
    similar to thinking_animation.
    """
    message = "Processing results"
    start_time = time.time()
    dot_sequence = [".", "..", "..."]

    i = 0
    while time.time() - start_time < duration:
        sys.stdout.write(f"\r{message}{dot_sequence[i % len(dot_sequence)]}")
        sys.stdout.flush()
        time.sleep(0.3)
        i += 1

    clear_line(message + "...")


def clear_line(previous_text: str):
    """
    Clears whatever was previously printed on the line.
    """
    # Overwrite the same number of characters with spaces, then carriage return
    sys.stdout.write("\r" + " " * len(previous_text) + "\r")
    sys.stdout.flush()
