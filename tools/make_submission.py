"""Build the three course submission files from the current repository.

Install python-docx and python-pptx first. The report PDF is a draft until the
team replaces VIDEO_URL_PENDING_PUBLIC_UPLOAD with its public YouTube URL.
"""

from pathlib import Path
import os
import re
import subprocess
import zipfile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import Inches as DocxInches, Pt as DocxPt, RGBColor as DocxRGBColor
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/REPORT_DRAFT.md"
TEMPLATE = Path(os.environ.get(
    "OUR_GAME_REPORT_TEMPLATE",
    "/home/sadow/Downloads/Computer Graphics Fundamentals report template.docx",
))
SUBMISSION = ROOT.parent / "our-game-submission"
EDITABLE = ROOT.parent / "our-game-submission-editable"
VIDEO_TOKEN = "VIDEO_URL_PENDING_PUBLIC_UPLOAD"
VIDEO_URL = os.environ.get("OUR_GAME_YOUTUBE_URL", VIDEO_TOKEN)


def plain(text):
    return text.replace("**", "").replace("`", "").replace("*", "")


def make_report():
    doc = Document(TEMPLATE)
    for name in ("Normal", "Heading 1", "Heading 2", "Title"):
        style = doc.styles[name]
        style.font.name = "Times New Roman"
        style.font.size = DocxPt(12)
        style.font.color.rgb = DocxRGBColor(0, 0, 0)
        if name != "Normal":
            style.font.bold = True
    doc.styles["Heading 1"].paragraph_format.space_before = DocxPt(12)
    doc.styles["Heading 2"].paragraph_format.space_before = DocxPt(8)
    # Keep the supplied title page and its university artwork; replace its fields.
    for paragraph in list(doc.paragraphs)[12:]:
        paragraph._element.getparent().remove(paragraph._element)
    replacements = {
        "Course Name:": "Computer Graphics Fundamentals (OKG 2214)",
        "Project Title:": "Orbit Bullet Hell",
        "Team Members:": "Mukhammed Sailau and Ali Turlas, IT-2507",
        "Instructor:": "Saleshova Sabina",
        "Date of Submission:": "9 November 2026",
    }
    for paragraph in doc.paragraphs:
        for start, value in replacements.items():
            if paragraph.text.startswith(start):
                # The template's first run is a bold field label. Keep it.
                for run in paragraph.runs[1:]:
                    run.text = ""
                paragraph.runs[1].text = " " + value
    doc.add_paragraph("Public YouTube demonstration: " + VIDEO_URL)
    doc.add_page_break()
    doc.add_heading("Table of Contents", 0)
    for title, page, level in (
        ("1. Introduction", 3, 0),
        ("2. Literature Review and Background", 3, 0),
        ("3. Project Description", 4, 0),
        ("3.1 Objective", 4, 1), ("3.2 Problem Statement", 4, 1),
        ("3.3 Scope and Rules", 4, 1),
        ("4. Technical Implementation", 5, 0),
        ("4.1 Tools and Technologies Used", 5, 1),
        ("4.2 Development Process and Teamwork", 5, 1),
        ("4.3 Algorithms and Techniques", 5, 1),
        ("5. Graphics and Rendering", 6, 0),
        ("5.1 2D and 3D Rendering", 6, 1),
        ("5.2 Lighting and Shading", 6, 1),
        ("5.3 Texturing and Animation", 6, 1),
        ("6. Testing and Evaluation", 6, 0),
        ("6.1 Testing Methodology", 6, 1),
        ("6.2 Performance Evaluation", 7, 1),
        ("6.3 Issues and Debugging", 7, 1),
        ("7. Conclusion and Future Work", 7, 0),
        ("8. References", 8, 0),
        ("9. Appendix", 9, 0),
    ):
        paragraph = doc.add_paragraph()
        if level:
            paragraph.paragraph_format.left_indent = DocxInches(0.25)
        paragraph.paragraph_format.tab_stops.add_tab_stop(
            DocxInches(6.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
        )
        run = paragraph.add_run(title + "\t" + str(page))
        run.bold = level == 0
    doc.add_page_break()

    in_body = False
    for raw in REPORT.read_text().replace(VIDEO_TOKEN, VIDEO_URL).splitlines():
        line = raw.strip()
        if line.startswith("## 1. Introduction"):
            in_body = True
        if not in_body or not line:
            continue
        if line.startswith("## "):
            if line.startswith("## 8. References"):
                doc.add_page_break()
            heading = doc.add_heading(line[3:], level=1)
            heading.paragraph_format.keep_with_next = True
        elif line.startswith("### "):
            heading = doc.add_heading(line[4:], level=2)
            heading.paragraph_format.keep_with_next = True
        elif line.startswith("!["):
            match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
            if match:
                doc.add_picture(str(ROOT / "docs" / match.group(2)), width=DocxInches(6.2))
                caption = doc.add_paragraph(match.group(1))
                caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in caption.runs:
                    run.italic = True
                    run.font.size = DocxPt(9)
        else:
            paragraph = doc.add_paragraph(plain(line))
            paragraph.paragraph_format.space_after = DocxPt(8)
            if line.startswith("["):
                paragraph.paragraph_format.left_indent = DocxInches(0.2)
                paragraph.paragraph_format.first_line_indent = DocxInches(-0.2)

    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.text = "Orbit Bullet Hell — IT-2507"
    output = EDITABLE / "Orbit_Bullet_Hell_Report_EDITABLE.docx"
    doc.save(output)
    final_pdf = SUBMISSION / "Orbit_Bullet_Hell_Report.pdf"
    final_pdf.unlink(missing_ok=True)
    result = subprocess.run(
        ["libreoffice", "-env:UserInstallation=file:///tmp/our-game-lo-profile",
         "--headless", "--convert-to", "pdf", "--outdir", str(SUBMISSION), str(output)],
        capture_output=True, text=True,
    )
    converted = SUBMISSION / output.with_suffix(".pdf").name
    if result.returncode == 0 and converted.exists():
        converted.replace(final_pdf)
    else:
        print("LibreOffice could not convert the DOCX here; export it to PDF manually.")
        print((result.stderr or result.stdout).strip())


BG = RGBColor(11, 13, 18)
PANEL = RGBColor(27, 31, 39)
WHITE = RGBColor(235, 235, 230)
MUTED = RGBColor(165, 172, 181)
RED = RGBColor(216, 66, 54)
GOLD = RGBColor(243, 179, 48)


def add_text(slide, text, x, y, w, h, size=22, color=WHITE, bold=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Inches(0.02)
    frame.margin_top = frame.margin_bottom = Inches(0.02)
    frame.text = text
    for paragraph in frame.paragraphs:
        paragraph.font.name = "DejaVu Sans"
        paragraph.font.size = Pt(size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = color
    return box


def base_slide(pres, title, number):
    slide = pres.slides.add_slide(pres.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BG
    add_text(slide, title, 0.65, 0.45, 12.1, 0.65, 30, WHITE, True)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(1.17), Inches(12), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = RED
    line.line.fill.background()
    add_text(slide, f"ORBIT BULLET HELL  •  IT-2507                                          {number:02d}",
             0.65, 7.08, 12, 0.25, 10, MUTED)
    return slide


def bullet(slide, text, y, x=0.8, width=11.8, color=WHITE):
    add_text(slide, "• " + text, x, y, width, 0.72, 22, color)


def make_slides():
    pres = Presentation()
    pres.slide_width = Inches(13.333)
    pres.slide_height = Inches(7.5)
    screenshot = ROOT / "docs/figures/gameplay.png"

    slide = base_slide(pres, "Orbit Bullet Hell", 1)
    add_text(slide, "A 60-second survival game in C++ and OpenGL 3.3", 0.7, 1.55, 12, 0.7, 25, GOLD)
    add_text(slide, "Mukhammed Sailau  •  Ali Turlas\nIT-2507  •  Saleshova Sabina", 0.7, 2.55, 6.0, 1.25, 21)
    slide.shapes.add_picture(str(screenshot), Inches(6.75), Inches(2.05), width=Inches(5.75))
    add_text(slide, "Computer Graphics Fundamentals", 0.7, 6.45, 8, 0.4, 18, MUTED)

    slide = base_slide(pres, "Game design and controls", 2)
    bullet(slide, "Survive 60 seconds across three 20-second waves.", 1.55)
    bullet(slide, "WASD moves; Shift slows; Space dashes; P pauses; R restarts.", 2.45)
    bullet(slide, "Aimed fans, radial rings, then rotating streams raise the challenge.", 3.35)
    bullet(slide, "Health, score, graze points, and the timer are visible in the HUD.", 4.25)
    bullet(slide, "Win by surviving; lose when health reaches zero.", 5.15, color=GOLD)

    slide = base_slide(pres, "Graphics pipeline from the lectures", 3)
    labels = ["C++ mesh + input", "VAO / VBO", "Vertex shader", "Fragment shader", "Framebuffer"]
    for i, label in enumerate(labels):
        x = 0.65 + i * 2.55
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                       Inches(x), Inches(2.1), Inches(2.18), Inches(1.0))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PANEL
        shape.line.color.rgb = GOLD if i == 3 else RED
        add_text(slide, label, x + 0.12, 2.33, 1.95, 0.5, 17)
        if i < 4:
            add_text(slide, "→", x + 2.22, 2.36, 0.3, 0.4, 20, GOLD)
    add_text(slide, "Model → view → projection positions the 3D scene.\nDepth testing draws nearer surfaces in front.\nThe HUD is blended after the 3D pass.",
             0.9, 3.8, 11.6, 1.8, 22)

    slide = base_slide(pres, "The actual running scene", 4)
    slide.shapes.add_picture(str(screenshot), Inches(2.65), Inches(1.45), width=Inches(8.0))
    add_text(slide, "Figure 1: actual third-wave OpenGL smoke capture", 2.65, 6.58, 8, 0.32, 15, MUTED)

    slide = base_slide(pres, "Geometry, camera, and shading", 5)
    bullet(slide, "Cube and generated sphere meshes use positions, normals, and UVs.", 1.55)
    bullet(slide, "Boss parent → orbit pivot → satellite → beacon inherit transforms.", 2.45)
    bullet(slide, "GLM builds model, lookAt view, and perspective projection matrices.", 3.35)
    bullet(slide, "The fragment shader adds ambient, diffuse, specular, and emission.", 4.25)
    add_text(slide, "Lectures L3–L5 and L9", 0.85, 5.8, 11, 0.4, 18, GOLD)

    slide = base_slide(pres, "Textures and animation", 6)
    bullet(slide, "C++ creates a 64×64 checker image and uploads it as an OpenGL texture.", 1.55)
    bullet(slide, "UV coordinates repeat the checker across the arena floor.", 2.45)
    bullet(slide, "World-space grid lines add a small procedural visual effect.", 3.35)
    bullet(slide, "Time animates the boss; amber, blue, and magenta mark the waves.", 4.25)
    add_text(slide, "Lectures L8–L10", 0.85, 5.8, 11, 0.4, 18, GOLD)

    slide = base_slide(pres, "Gameplay code: small, testable rules", 7)
    bullet(slide, "The game updates at a fixed 120 steps per second.", 1.55)
    bullet(slide, "A bullet moves by velocity × time step.", 2.45)
    bullet(slide, "Squared distances detect hits and near misses.", 3.35)
    bullet(slide, "Timers control waves, dash cooldown, and damage grace time.", 4.25)
    bullet(slide, "Old bullets leave the arena and are removed.", 5.15, color=GOLD)

    slide = base_slide(pres, "Testing and measured performance", 8)
    bullet(slide, "Rules test covers movement, collision, dash, graze, pause, restart, and win/loss.", 1.55)
    bullet(slide, "Three wave smoke checks drew 360 frames each with no GL errors.", 2.65)
    bullet(slide, "Final wave 3: 133.8 frames/s, 206.5 MiB max RSS, 105 shots.", 3.75)
    bullet(slide, "Smaller sphere mesh: 384 triangles instead of 1,120 per shot.", 4.85)
    add_text(slide, "Single-run Xvfb software rendering at 1280×800.", 0.85, 6.0, 11.8, 0.35, 18, GOLD)

    slide = base_slide(pres, "Teamwork and academic integrity", 9)
    bullet(slide, "Mukhammed: gameplay, tests, integration, report and presentation drafts.", 1.55)
    bullet(slide, "Ali: hierarchical boss and wave visuals in main.cpp; rendering checks.", 2.55)
    bullet(slide, "Both retain original Git history and commit under their own identities.", 3.55)
    bullet(slide, "Codex assisted both students with code, testing, and documents.", 4.55)
    add_text(slide, "Every submitted result needs student review and explanation.",
             0.85, 5.75, 11.8, 0.55, 20, GOLD)

    slide = base_slide(pres, "Demonstration and references", 10)
    add_text(slide, "Public 3–6 minute YouTube demo:", 0.85, 1.55, 11.5, 0.45, 23, WHITE, True)
    add_text(slide, VIDEO_URL, 0.85, 2.2, 11.8, 0.5, 20, GOLD)
    add_text(slide, "The PDF report contains 15 journal references with DOI links.\nKey background: Gouraud (1971), Phong (1975), Blinn and Newell (1976),\nPerlin (2002), and the graphics surveys listed in the report.",
             0.85, 3.35, 11.6, 1.8, 20)
    add_text(slide, "Source and coordination: github.com/Csadow/our-game-continued", 0.85, 6.05, 11.8, 0.4, 17, MUTED)

    pres.save(SUBMISSION / "Orbit_Bullet_Hell_Presentation.pptx")


def make_source_zip():
    included = ["README.md", "CMakeLists.txt", "game.h", "game.cpp", "game_tests.cpp",
                "main.cpp", "scene.vert", "scene.frag", "hud.vert", "hud.frag"]
    with zipfile.ZipFile(SUBMISSION / "Orbit_Bullet_Hell_Source.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(included):
            archive.write(ROOT / name, "Orbit_Bullet_Hell/" + name)


if __name__ == "__main__":
    SUBMISSION.mkdir(exist_ok=True)
    EDITABLE.mkdir(exist_ok=True)
    make_report()
    make_slides()
    make_source_zip()
    print("Generated presentation and source ZIP in", SUBMISSION)
    print("Editable report:", EDITABLE / "Orbit_Bullet_Hell_Report_EDITABLE.docx")
    if VIDEO_URL == VIDEO_TOKEN:
        print("DRAFT: add OUR_GAME_YOUTUBE_URL after the public upload, then regenerate.")
