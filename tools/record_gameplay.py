"""Record an actual game session on Xvfb with simple scripted key presses.

Run with: xvfb-run -a -s '-screen 0 1280x800x24' python tools/record_gameplay.py
Requires python-xlib and ffmpeg. The clip is silent; see demo script for narration.
"""

from pathlib import Path
import os
import subprocess
import time

from Xlib import X, XK, display
from Xlib.ext import xtest


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent / "our-game-submission-editable/gameplay_capture.mp4"


def find_window(server):
    for _ in range(50):
        for child in server.screen().root.query_tree().children:
            if "Orbit" in (child.get_wm_name() or ""):
                return child
        time.sleep(0.1)
    raise RuntimeError("The Orbit window did not appear on the X display.")


def key(server, name, pressed):
    symbol = XK.string_to_keysym(name)
    code = server.keysym_to_keycode(symbol)
    xtest.fake_input(server, X.KeyPress if pressed else X.KeyRelease, code)
    server.sync()


def hold(server, names, seconds):
    for name in names:
        key(server, name, True)
    time.sleep(seconds)
    for name in reversed(names):
        key(server, name, False)


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    if not os.environ.get("DISPLAY"):
        raise RuntimeError("Start this script under xvfb-run.")
    game = subprocess.Popen([str(ROOT / "build/bullethell")], cwd=ROOT)
    server = display.Display()
    try:
        window = find_window(server)
        window.set_input_focus(X.RevertToParent, X.CurrentTime)
        server.sync()
        recording = subprocess.Popen([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "x11grab", "-framerate", "15", "-video_size", "1280x800",
            "-i", os.environ["DISPLAY"], "-t", "73",
            "-vf", "scale=960:600", "-c:v", "libx264", "-preset", "ultrafast",
            "-crf", "26", "-pix_fmt", "yuv420p", str(OUTPUT),
        ])
        # Without a window manager, GLFW sees an initial focus loss on Xvfb.
        # Resume after focusing the game window so the first seconds show play.
        time.sleep(0.25)
        hold(server, ["p"], 0.1)
        # Show movement, precision mode, dashing, pause, death, and restart.
        # A restart halfway through keeps action visible if the first run ends.
        sequence = [
            ([], 2), (["a", "Shift_L"], 4), (["d", "Shift_L"], 7),
            (["w", "a"], 4), (["space", "d"], 0.25), (["d"], 5),
            (["s", "a"], 5), (["p"], 0.1), ([], 2), (["p"], 0.1),
            (["w", "d"], 5), (["a"], 5), (["r"], 0.1),
            (["d", "Shift_L"], 7), (["w", "a"], 6),
            (["space", "d"], 0.25), (["s", "d"], 7),
            (["a", "Shift_L"], 7), ([], 5),
        ]
        for names, seconds in sequence:
            if game.poll() is not None:
                raise RuntimeError("The game closed while recording.")
            hold(server, names, seconds)
        key(server, "Escape", True)
        key(server, "Escape", False)
        if recording.wait(timeout=20):
            raise RuntimeError("ffmpeg could not capture the X display.")
    finally:
        server.close()
        if game.poll() is None:
            game.terminate()
        game.wait(timeout=5)
    print("Recorded", OUTPUT)


if __name__ == "__main__":
    main()
