"""Build the three course submission files from the current repository.

Install python-docx and python-pptx first. The report PDF is a draft until the
team replaces VIDEO_URL_PENDING_PUBLIC_UPLOAD with its public YouTube URL.
"""

from pathlib import Path
import re
import subprocess
import zipfile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches as DocxInches, Pt as DocxPt
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs/REPORT_DRAFT.md"
TEMPLATE = Path("/home/sadow/Downloads/Computer Graphics Fundamentals report template.docx")
SUBMISSION = ROOT.parent / "our-game-submission"
EDITABLE = ROOT.parent / "our-game-submission-editable"
VIDEO_TOKEN = "VIDEO_URL_PENDING_PUBLIC_UPLOAD"


def plain(text):
    return text.replace("**", "").replace("`", "").replace("*", "")


def make_report():
    doc = Document(TEMPLATE)
    # Keep the supplied title page and its university artwork; replace its fields.
    for paragraph in list(doc.paragraphs)[12:]:
        paragraph._element.getparent().remove(paragraph._element)
    replacements = {
        "Course Name:": "Course Name: Computer Graphics Fundamentals (OKG 2214)",
        "Project Title:": "Project Title: Orbit Bullet Hell",
        "Team Members:": "Team Members: Mukhammed Sailau and Ali Turlas, IT-2507",
        "Instructor:": "Instructor: Saleshova Sabina",
        "Date of Submission:": "Date of Submission: 9 November 2026",
    }
    for paragraph in doc.paragraphs:
        for start, value in replacements.items():
            if paragraph.text.startswith(start):
                paragraph.text = value
    doc.add_paragraph("Public YouTube demonstration: " + VIDEO_TOKEN)
    doc.add_page_break()
    doc.add_heading("Table of Contents", 0)
    for title in (
        "1. Introduction", "2. Literature Review and Background",
        "3. Project Description", "4. Technical Implementation",
        "5. Graphics and Rendering", "6. Testing and Evaluation",
        "7. Conclusion and Future Work", "8. References", "9. Appendix",
    ):
        doc.add_paragraph("• " + title, style="List Paragraph")
    doc.add_page_break()

    in_body = False
    for raw in REPORT.read_text().splitlines():
        line = raw.strip()
        if line.startswith("## 1. Introduction"):
            in_body = True
        if not in_body or not line:
            continue
        if line.startswith("## "):
            if line.startswith("## 8. References"):
                doc.add_page_break()
            doc.add_heading(line[3:], level=1)
        elif line.startswith("### "):
            doc.add_heading(line[4:], level=2)
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
    result = subprocess.run(
        ["libreoffice", "-env:UserInstallation=file:///tmp/our-game-lo-profile",
         "--headless", "--convert-to", "pdf", "--outdir", str(SUBMISSION), str(output)],
        capture_output=True, text=True,
    )
    converted = SUBMISSION / output.with_suffix(".pdf").name
    if result.returncode == 0 and converted.exists():
        converted.rename(SUBMISSION / "Orbit_Bullet_Hell_Report.pdf")
    else:
        print("LibreOffice could not convert the DOCX here; export it to PDF manually.")


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
    add_text(slide, "Figure 1: captured from the 360-frame OpenGL smoke test", 2.65, 6.58, 8, 0.32, 15, MUTED)

    slide = base_slide(pres, "Geometry, camera, and shading", 5)
    bullet(slide, "Cube and generated sphere meshes use positions, normals, and UVs.", 1.55)
    bullet(slide, "GLM builds model, lookAt view, and perspective projection matrices.", 2.45)
    bullet(slide, "One fragment shader adds ambient, diffuse, specular, and emission.", 3.35)
    bullet(slide, "A simple local light keeps the shapes readable during play.", 4.25)
    add_text(slide, "Lectures L3–L5 and L9", 0.85, 5.8, 11, 0.4, 18, GOLD)

    slide = base_slide(pres, "Textures and animation", 6)
    bullet(slide, "C++ creates a 64×64 checker image and uploads it as an OpenGL texture.", 1.55)
    bullet(slide, "UV coordinates repeat the checker across the arena floor.", 2.45)
    bullet(slide, "World-space grid lines add a small procedural visual effect.", 3.35)
    bullet(slide, "Sine movement and timers animate the boss and projectile patterns.", 4.25)
    add_text(slide, "Lectures L8–L10", 0.85, 5.8, 11, 0.4, 18, GOLD)

    slide = base_slide(pres, "Gameplay code: small, testable rules", 7)
    bullet(slide, "The game updates at a fixed 120 steps per second.", 1.55)
    bullet(slide, "A bullet moves by velocity × time step.", 2.45)
    bullet(slide, "Squared distances detect hits and near misses.", 3.35)
    bullet(slide, "Timers control waves, dash cooldown, and damage grace time.", 4.25)
    bullet(slide, "Old bullets leave the arena and are removed.", 5.15, color=GOLD)

    slide = base_slide(pres, "Testing and measured performance", 8)
    bullet(slide, "Rules test covers movement, collision, dash, graze, pause, restart, and win/loss.", 1.55)
    bullet(slide, "OpenGL smoke test drew 360 frames with no GL errors.", 2.65)
    bullet(slide, "One Xvfb + Mesa llvmpipe run: 88.2 frames/s, 205 MiB max RSS.", 3.75)
    bullet(slide, "Software rendering at 1280×800; not a GPU benchmark.", 4.85, color=GOLD)

    slide = base_slide(pres, "Teamwork and academic integrity", 9)
    bullet(slide, "Mukhammed: gameplay, tests, integration, report and presentation drafts.", 1.55)
    bullet(slide, "Ali: rendering, hierarchical boss model, shaders, and visual review (in progress).", 2.55)
    bullet(slide, "Both retain original Git history and commit under their own identities.", 3.55)
    bullet(slide, "Codex assisted with planning, code suggestions, testing, and documents.", 4.55)
    add_text(slide, "Every submitted result needs student review and explanation.",
             0.85, 5.75, 11.8, 0.55, 20, GOLD)

    slide = base_slide(pres, "Demonstration and references", 10)
    add_text(slide, "Public 3–6 minute YouTube demo:", 0.85, 1.55, 11.5, 0.45, 23, WHITE, True)
    add_text(slide, VIDEO_TOKEN, 0.85, 2.2, 11.8, 0.5, 20, GOLD)
    add_text(slide, "The PDF report contains 15 journal references with DOI links.\nKey background: Gouraud (1971), Phong (1975), Blinn and Newell (1976),\nPerlin (2002), and the graphics surveys listed in the report.",
             0.85, 3.35, 11.6, 1.8, 20)
    add_text(slide, "Source and coordination: github.com/Csadow/our-game-continued", 0.85, 6.05, 11.8, 0.4, 17, MUTED)

    pres.save(SUBMISSION / "Orbit_Bullet_Hell_Presentation.pptx")


def make_source_zip():
    included = ["README.md", "CMakeLists.txt", "game.h", "game.cpp", "game_tests.cpp",
                "main.cpp", "scene.vert", "scene.frag", "hud.vert", "hud.frag"]
    included += [str(path.relative_to(ROOT)) for path in (ROOT / "docs").rglob("*") if path.is_file()]
    included += [str(path.relative_to(ROOT)) for path in (ROOT / "tools").rglob("*") if path.is_file()]
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
