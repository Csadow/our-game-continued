"""Combine the real gameplay capture with readable source-code walkthrough cards.

Requires Pillow and ffmpeg. Output is a silent MP4 for the students to review,
narrate if desired, and upload publicly to YouTube.
"""

from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EDITABLE = ROOT.parent / "our-game-submission-editable"
CAPTURE = EDITABLE / "gameplay_capture.mp4"
OUTPUT = EDITABLE / "Orbit_Bullet_Hell_Demo_Draft.mp4"
FONT = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
MONO = "/usr/share/fonts/noto/NotoSansMono-Regular.ttf"


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


def snippet(file, start, count):
    lines = (ROOT / file).read_text().splitlines()
    first = next((i for i, line in enumerate(lines) if start in line), None)
    if first is None:
        raise ValueError(f"Could not find {start!r} in {file}")
    return "\n".join(lines[first:first + count])


def font(path, size):
    return ImageFont.truetype(path, size)


def card(path, title, description, code=""):
    image = Image.new("RGB", (960, 600), (11, 13, 18))
    draw = ImageDraw.Draw(image)
    draw.text((38, 30), title, font=font(FONT, 31), fill=(238, 238, 232))
    draw.rectangle((38, 85, 922, 88), fill=(216, 66, 54))
    draw.multiline_text((40, 105), description, font=font(FONT, 20),
                        fill=(243, 179, 48), spacing=5)
    if code:
        draw.rounded_rectangle((35, 185, 925, 555), 10, fill=(27, 31, 39))
        code_size = 14 if len(code.splitlines()) > 14 else 16
        draw.multiline_text((50, 198), code, font=font(MONO, code_size),
                            fill=(218, 224, 225), spacing=3)
    else:
        draw.text((40, 540), "Mukhammed Sailau • Ali Turlas • IT-2507",
                  font=font(FONT, 15), fill=(165, 172, 181))
    image.save(path)


def wave_card(path, wave):
    source = ROOT / "docs/figures" / f"wave-{wave}.png"
    image = Image.open(source).convert("RGB").resize((960, 600))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 960, 92), fill=(11, 13, 18))
    draw.text((28, 12), f"Wave {wave} — labeled rendering check",
              font=font(FONT, 29), fill=(238, 238, 232))
    explanation = ("Blue boss and HUD; cyan rotating shots start at 20 seconds."
                   if wave == 2 else
                   "Magenta boss and HUD; opposite cyan streams at 40 seconds.")
    draw.text((30, 54), explanation, font=font(FONT, 18), fill=(243, 179, 48))
    draw.rectangle((0, 564, 960, 600), fill=(11, 13, 18))
    draw.text((30, 572), "Test shortcut starts at the wave boundary; not a full playthrough.",
              font=font(FONT, 15), fill=(216, 222, 224))
    image.save(path)


def still_video(image, seconds, output):
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-loop", "1", "-framerate", "15", "-i", str(image),
         "-t", str(seconds), "-c:v", "libx264", "-preset", "ultrafast",
         "-crf", "25", "-pix_fmt", "yuv420p", str(output)])


def main():
    if not CAPTURE.exists():
        raise FileNotFoundError("Record gameplay first with tools/record_gameplay.py")
    EDITABLE.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="our-game-demo-") as temporary:
        folder = Path(temporary)
        cards = [
            ("Orbit Bullet Hell", "Actual gameplay, labeled wave checks, then the C++ and GLSL source.\nControls: WASD move, Shift slow, Space dash, P pause, R restart.", "", 12),
            ("Fixed update and movement", "game.cpp: 120 updates per second keep movement stable.",
             snippet("game.cpp", "// A fixed 120 Hz step", 16), 23),
            ("Projectile collision", "game.cpp: squared distances test hits without a square root.",
             snippet("game.cpp", "const float hitDistance", 15), 23),
            ("3D transformation pipeline", "scene.vert: model, view, and projection place vertices on screen.",
             snippet("scene.vert", "uniform mat4 model", 15), 23),
            ("Hierarchical boss model", "main.cpp: the boss parent carries orbit pivots, satellites, and beacons.",
             snippet("main.cpp", "glm::mat4 bossParent", 19), 23),
            ("Lighting in the fragment shader", "scene.frag: ambient, diffuse, specular, and emission.",
             snippet("scene.frag", "vec3 N =", 12), 23),
            ("Tests and three waves", "game_tests.cpp: checks keep the second and third waves distinct.",
             snippet("game_tests.cpp", "Game waveTwo;", 19), 23),
            ("What to review", "Build and run from the ZIP source; read the PDF report for methods,\nmeasurements, AI-use disclosure, and 15 journal references.", "", 12),
        ]
        segments = []
        for index, (title, description, code, duration) in enumerate(cards):
            picture = folder / f"card-{index}.png"
            video = folder / f"card-{index}.mp4"
            card(picture, title, description, code)
            still_video(picture, duration, video)
            segments.append(video)
            if index == 0:
                segments.append(CAPTURE)
                for wave in (2, 3):
                    wave_picture = folder / f"wave-{wave}.png"
                    wave_video = folder / f"wave-{wave}.mp4"
                    wave_card(wave_picture, wave)
                    still_video(wave_picture, 14, wave_video)
                    segments.append(wave_video)
        listing = folder / "segments.txt"
        listing.write_text("".join(f"file '{path}'\n" for path in segments))
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-f", "concat", "-safe", "0", "-i", str(listing),
             "-c", "copy", "-movflags", "+faststart", str(OUTPUT)])
    print("Demo video:", OUTPUT)


if __name__ == "__main__":
    main()
