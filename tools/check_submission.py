"""Check the three exported course files without modifying them.

Requires pypdf for PDF text extraction. Public YouTube visibility, document
layout, and a human playtest must be checked separately.
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


SOURCE_FILES = {
    "README.md", "CMakeLists.txt", "game.h", "game.cpp", "game_tests.cpp",
    "main.cpp", "scene.vert", "scene.frag", "hud.vert", "hud.frag",
}
VIDEO = re.compile(
    r"https?://(?:www\.)?(?:youtu\.be/|youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})"
)
PLACEHOLDERS = ("VIDEO_URL_PENDING_PUBLIC_UPLOAD", "[Insert Project Title]",
                "[Insert Names and group]", "[Insert Date]")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Directory containing the three exports")
    parser.add_argument("--expected-slides", type=int, default=10)
    args = parser.parse_args()
    errors = []
    texts = {}
    for suffix, label in (("pdf", "Report"), ("pptx", "Presentation"), ("zip", "Source")):
        path = args.directory / f"Orbit_Bullet_Hell_{label}.{suffix}"
        if not path.is_file():
            errors.append(f"Missing {path.name}")
            continue
        try:
            if suffix == "pdf":
                from pypdf import PdfReader
                reader = PdfReader(path)
                if not reader.pages:
                    raise ValueError("Report contains no pages")
                texts[label] = "\n".join(page.extract_text() or "" for page in reader.pages)
            else:
                with zipfile.ZipFile(path) as archive:
                    bad = archive.testzip()
                    if bad:
                        raise ValueError(f"Corrupt ZIP entry {bad}")
                    if suffix == "pptx":
                        slides = [n for n in archive.namelist()
                                  if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
                        if len(slides) != args.expected_slides:
                            errors.append(f"Expected {args.expected_slides} slides, found {len(slides)}")
                        parts = slides + [n for n in archive.namelist()
                                          if n.startswith("ppt/slides/_rels/") and n.endswith(".rels")]
                        texts[label] = "\n".join(
                            " ".join(ElementTree.fromstring(archive.read(n)).itertext())
                            + " " + archive.read(n).decode("utf-8") for n in parts
                        )
                    else:
                        names = archive.namelist()
                        expected = {f"Orbit_Bullet_Hell/{name}" for name in SOURCE_FILES}
                        missing = sorted(expected - set(names))
                        if missing:
                            errors.append("Source ZIP missing: " + ", ".join(missing))
                        for name in names:
                            parts = Path(name).parts
                            if name.startswith("/") or ".." in parts or any(
                                part == ".git" or part == ".ssh" or part.startswith("build")
                                for part in parts
                            ):
                                errors.append(f"Unwanted source ZIP entry: {name}")
            print(f"Read {path.name}")
        except (OSError, ValueError, ImportError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
            errors.append(f"Cannot inspect {path.name}: {exc}")

    ids = {}
    for label, text in texts.items():
        for placeholder in PLACEHOLDERS:
            if placeholder in text:
                errors.append(f"{label} still contains {placeholder}")
        # PDF text may wrap a URL over lines. Also inspect PPTX hyperlink XML.
        compact = re.sub(r"\s+", "", text)
        ids[label] = set(VIDEO.findall(compact))
        if not ids[label]:
            errors.append(f"{label} has no recognizable YouTube demonstration URL")
    if ids.get("Report") and ids.get("Presentation") and not (
        ids["Report"] & ids["Presentation"]
    ):
        errors.append("Report and presentation do not share the same YouTube video ID")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("File checks passed. Separately verify public video visibility, exported layout and human playtest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
