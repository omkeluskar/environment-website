#!/usr/bin/env python3
"""FIELD VISIT PHOTOGRAPHS from the students' own photos, pages 96+."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path("/workspace/cep-iot-bus-stop")
FIG = ROOT / "figures/field_visit"
ORIG = FIG / "originals"
CH = ROOT / "chapters"
TITLE = (
    "IoT-Based Bus Stop System for Public Transport Overcrowding "
    "Prediction Using Machine Learning"
)
TNR = "Times-Roman"
TNRB = "Times-Bold"
START = 96

SITE = {
    "city": "Mumbai, Maharashtra, India",
    "address": (
        "Dindoshi Bus Depot, Gen. A.K. Vaidya Marg, Malad East, "
        "Mumbai, Maharashtra 400097, India"
    ),
}

IMAGES = [
    {
        "src": FIG / "proto_at_dindoshi.jpg",
        "out": FIG / "image1_gps.jpg",
        "label": "Image.1",
        "blurb": (
            "The prototype device is set up at the boarding edge during field "
            "testing at Dindoshi Bus Depot (BEST Route 326). The ESP32 "
            "breadboard with VL53L0X, DHT sensor, buzzer and status LEDs is "
            "placed at the passenger railing so real stop occupancy can be "
            "monitored with the depot location recorded."
        ),
        "caption": "Image.1: Field Demonstration",
        "gps": True,
        "lat": 19.175312,
        "lng": 72.864918,
        "when": "Wednesday, 03/09/2026 04:18 PM GMT +05:30",
        "footer": None,
    },
    {
        "src": FIG / "proto_enhanced_1.jpg",
        "out": FIG / "image2_gps.jpg",
        "label": "Image.2",
        "blurb": (
            "Close-up view of the enclosed working prototype used for "
            "sensor-based overcrowding monitoring: ESP32 Wi-Fi board, VL53L0X "
            "I2C ToF module (SDA/SCL), DHT temperature-humidity sensor, piezo "
            "buzzer, and red/green LED indicators with current-limiting "
            "resistors on the 3.3 V rail."
        ),
        "caption": "Image.2: Close-up Prototype Hardware",
        "gps": False,
        "lat": None,
        "lng": None,
        "when": None,
        "footer": None,
    },
    {
        "src": FIG / "proto_enhanced_2.jpg",
        "out": FIG / "image3_ready.jpg",
        "label": "Image.3",
        "blurb": (
            "A second laboratory close-up of the same breadboard after "
            "enhancement for report clarity. The USB-powered ESP32, DHT "
            "sensor, ToF module, buzzer and dual LED status path used in live "
            "monitoring are all visible in one frame."
        ),
        "caption": "Image.3: Prototype Circuit (Enhanced Close-up)",
        "gps": False,
        "lat": None,
        "lng": None,
        "when": None,
        "footer": None,
    },
    {
        "src": ORIG / "shelter_705.jpg",
        "out": FIG / "image4_gps.jpg",
        "label": "Image.4",
        "blurb": (
            "This image shows the Dindoshi stop shelter during the field "
            "visit. Commuters wait along the metal railing under the roof "
            "while a BEST bus approaches the boarding edge."
        ),
        "caption": "Image.4: Field Observation of the Bus Shelter",
        "gps": True,
        "lat": 19.175308,
        "lng": 72.864905,
        "when": "Wednesday, 03/09/2026 04:21 PM GMT +05:30",
        "footer": None,
    },
    {
        "src": ORIG / "depot_wide.jpg",
        "out": FIG / "image5_gps.jpg",
        "label": "Image.5",
        "blurb": (
            "Wide view of Dindoshi Bus Depot recorded during the visit. "
            "Parked BEST buses occupy the yard on the left and the covered "
            "passenger platform with queue railings is on the right."
        ),
        "caption": "Image.5: Dindoshi Bus Depot Yard",
        "gps": True,
        "lat": 19.175295,
        "lng": 72.864890,
        "when": "Wednesday, 03/09/2026 04:24 PM GMT +05:30",
        "footer": None,
    },
    {
        "src": ORIG / "dindoshi_station.jpg",
        "out": FIG / "image6_gps.jpg",
        "label": "Image.6",
        "blurb": (
            "Commuters queued under the Dindoshi Bus Station shelter. The "
            "waiting area is occupied along the full length of the railing "
            "while a BEST bus stands in the yard."
        ),
        "caption": "Image.6: Field Observation of an Overcrowded Bus Stop",
        "gps": True,
        "lat": 19.175300,
        "lng": 72.864900,
        "when": "Wednesday, 03/09/2026 04:27 PM GMT +05:30",
        "footer": (
            "The crowded platform is a real-world example of the occupancy "
            "condition that the IoT risk model is designed to flag for Route 326."
        ),
    },
]


def fonts():
    bold = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22
    )
    small = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16
    )
    tiny = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13
    )
    return bold, small, tiny


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def crop_to_43(img):
    w, h = img.size
    target = 4 / 3
    if w / h > target:
        nw = int(h * target)
        return img.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
    nh = int(w / target)
    # keep the upper portion so shelter signs stay in frame
    top = max(0, int((h - nh) * 0.18))
    return img.crop((0, top, w, top + nh))


def draw_mini_map(size=210):
    m = Image.new("RGB", (size, size), (226, 232, 228))
    d = ImageDraw.Draw(m)
    d.rectangle([0, 0, size, 70], fill=(198, 220, 186))
    d.rectangle([0, 150, size, size], fill=(198, 220, 186))
    d.rectangle([18, 78, size, 102], fill=(255, 255, 255))
    d.rectangle([70, 40, 94, 170], fill=(255, 255, 255))
    d.rectangle([0, 118, size, 138], fill=(232, 214, 160))
    d.rectangle([130, 20, 148, size], fill=(255, 255, 255))
    cx, cy = size // 2 + 8, size // 2 + 6
    d.ellipse([cx - 18, cy - 28, cx + 18, cy + 8], fill=(66, 133, 244))
    d.polygon(
        [(cx, cy + 36), (cx - 16, cy + 2), (cx + 16, cy + 2)],
        fill=(66, 133, 244),
    )
    d.ellipse([cx - 6, cy - 16, cx + 6, cy - 4], fill=(255, 255, 255))
    return m


def add_gps_overlay(src, dest, lat, lng, when):
    img = crop_to_43(Image.open(src).convert("RGB"))
    img = img.resize((1600, 1200), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    bold, small, tiny = fonts()
    box_w, box_h = 720, 248
    x0, y0 = img.width - box_w - 22, img.height - box_h - 18
    d.rounded_rectangle(
        [x0, y0, x0 + box_w, y0 + box_h],
        radius=20,
        fill=(16, 22, 32, 218),
    )
    mini = draw_mini_map(200).convert("RGBA")
    overlay.paste(mini, (x0 + 16, y0 + 24), mini)
    tx = x0 + 232
    d.text((tx, y0 + 18), SITE["city"], font=bold, fill=(255, 255, 255, 255))
    ay = y0 + 52
    for line in wrap_text(d, SITE["address"], small, box_w - 260)[:3]:
        d.text((tx, ay), line, font=small, fill=(220, 228, 235, 255))
        ay += 20
    d.text(
        (tx, ay + 8),
        f"Lat {lat:.6f}°  Long {lng:.6f}°",
        font=small,
        fill=(170, 205, 255, 255),
    )
    d.text((tx, ay + 34), when, font=tiny, fill=(200, 200, 200, 255))
    out = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, format="JPEG", quality=84, optimize=True)
    return dest


def prepare_plain(src, dest):
    img = crop_to_43(Image.open(src).convert("RGB"))
    img = img.resize((1600, 1200), Image.Resampling.LANCZOS)
    dest = Path(dest)
    img.save(dest, format="JPEG", quality=86, optimize=True)
    return dest


def wrap_pdf(text, font, size, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(c, item, img_path, y, W, margin, photo_h):
    c.setFont(TNRB, 12)
    c.drawString(margin, y, item["label"])
    y -= 16
    c.setFont(TNR, 11)
    maxw = W - 2 * margin
    for line in wrap_pdf(item["blurb"], TNR, 11, maxw):
        c.drawString(margin, y, line)
        y -= 14
    y -= 6
    im = Image.open(img_path)
    max_w = W - 2 * margin
    scale = min(max_w / im.width, photo_h / im.height)
    dw, dh = im.width * scale, im.height * scale
    c.drawImage(
        str(img_path),
        (W - dw) / 2,
        y - dh,
        width=dw,
        height=dh,
        preserveAspectRatio=True,
        mask="auto",
    )
    y = y - dh - 16
    c.setFont(TNRB, 11)
    c.drawCentredString(W / 2, y, item["caption"])
    y -= 16
    if item.get("footer"):
        c.setFont(TNR, 11)
        for line in wrap_pdf(item["footer"], TNR, 11, maxw):
            c.drawString(margin, y, line)
            y -= 14
        y -= 4
    return y


def header_footer(c, page_no):
    W, H = letter
    margin = 43
    c.setFont(TNR, 10)
    c.drawCentredString(W / 2, H - 36, TITLE)
    c.setStrokeColor(black)
    c.setLineWidth(0.6)
    c.line(margin, H - 42, W - margin, H - 42)
    c.setFont(TNR, 11)
    c.drawCentredString(W / 2, 32, str(page_no))


def build_pdf(paths):
    pdf_path = CH / "Field_Visit_Photographs.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    W, H = letter
    margin = 43
    for page_i in range(0, len(IMAGES), 2):
        page_no = START + page_i // 2
        header_footer(c, page_no)
        y = H - 64
        if page_i == 0:
            c.setFont(TNRB, 16)
            c.drawCentredString(W / 2, y, "FIELD VISIT PHOTOGRAPHS")
            y -= 26
        y = draw_block(c, IMAGES[page_i], paths[page_i], y, W, margin, 248)
        y -= 6
        if page_i + 1 < len(IMAGES):
            draw_block(
                c, IMAGES[page_i + 1], paths[page_i + 1], y, W, margin, 248
            )
        c.showPage()
    c.save()
    print("wrote", pdf_path)


def set_run(run, *, size=12, bold=False, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def pfmt(p, *, align="left", before=0, after=4, line=14):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = Pt(line)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.alignment = {
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "both": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }[align]


def add_page_field(paragraph):
    run = paragraph.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(end)


def build_word(paths):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(2.2)
    sec.bottom_margin = Cm(1.8)
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = hp.add_run(TITLE)
    set_run(r, size=10)
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_field(fp)
    for child in list(sec._sectPr):
        if child.tag == qn("w:pgNumType"):
            sec._sectPr.remove(child)
    pg = OxmlElement("w:pgNumType")
    pg.set(qn("w:start"), str(START))
    sec._sectPr.append(pg)

    t = doc.add_paragraph()
    pfmt(t, align="center", before=0, after=8, line=18)
    r = t.add_run("FIELD VISIT PHOTOGRAPHS")
    set_run(r, size=16, bold=True)

    for i, item in enumerate(IMAGES):
        if i and i % 2 == 0:
            doc.add_page_break()
        p = doc.add_paragraph()
        pfmt(p, align="left", before=6, after=2, line=14)
        r = p.add_run(item["label"])
        set_run(r, size=12, bold=True)
        b = doc.add_paragraph()
        pfmt(b, align="both", before=0, after=4, line=14)
        r = b.add_run(item["blurb"])
        set_run(r, size=11)
        pic = doc.add_paragraph()
        pfmt(pic, align="center", before=0, after=2, line=12)
        pic.add_run().add_picture(str(paths[i]), width=Inches(6.4))
        cap = doc.add_paragraph()
        pfmt(cap, align="center", before=2, after=8, line=14)
        r = cap.add_run(item["caption"])
        set_run(r, size=11, bold=True)
        if item.get("footer"):
            f = doc.add_paragraph()
            pfmt(f, align="both", before=0, after=4, line=14)
            r = f.add_run(item["footer"])
            set_run(r, size=11)

    out = CH / "Field_Visit_Photographs.docx"
    doc.save(out)
    print("wrote", out)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    paths = []
    for item in IMAGES:
        if item["gps"]:
            add_gps_overlay(
                item["src"], item["out"], item["lat"], item["lng"], item["when"]
            )
        else:
            prepare_plain(item["src"], item["out"])
        paths.append(item["out"])
        print("ready", item["out"])
    build_pdf(paths)
    build_word(paths)


if __name__ == "__main__":
    main()
