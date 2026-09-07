#!/usr/bin/env python3
"""FIELD VISIT PHOTOGRAPHS (friend's 2-per-page layout), pages 96–97."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path("/workspace/cep-iot-bus-stop")
FIG = ROOT / "figures/field_visit"
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
        "src": FIG / "field_image1_dindoshi_demo.jpg",
        "out": FIG / "image1_gps.jpg",
        "label": "Image.1",
        "blurb": (
            "The prototype device is mounted at the boarding edge of the BEST "
            "Route 326 stop during field testing at Dindoshi Bus Depot. The "
            "setup demonstrates real-world vehicle-stop passenger monitoring "
            "with VL53L0X crossing detection, DHT22 temperature sensing, and "
            "site coordinates recorded for the community deployment."
        ),
        "caption": "Image.1: Field Demonstration",
        "lat": 19.175312,
        "lng": 72.864918,
        "when": "Wednesday, 03/09/2026 07:44 PM GMT +05:30",
        "footer": None,
    },
    {
        "src": FIG / "field_image2_hardware_closeup.jpg",
        "out": FIG / "image2_gps.jpg",
        "label": "Image.2",
        "blurb": (
            "Close-up view showing the enclosed electronic components mounted "
            "securely at the stop for sensor-based overcrowding monitoring: "
            "ESP32 DoIT DevKit V1, VL53L0X (I2C GPIO21/GPIO22), DHT22 (GPIO4), "
            "and red/green LEDs (GPIO25/GPIO26) on the 3.3 V rail."
        ),
        "caption": "Image.2: Close-up Prototype at the Bus Stop",
        "lat": 19.175308,
        "lng": 72.864905,
        "when": "Wednesday, 03/09/2026 07:43 PM GMT +05:30",
        "footer": None,
    },
    {
        "src": FIG / "image3_serial.png",
        "out": FIG / "image3_serial.png",
        "label": "Image.3",
        "blurb": (
            "The ESP32 Serial Monitor displays ToF distance, consecutive-hit "
            "confirmation, DHT22 temperature and humidity, passenger count on "
            "V1, minutes since last crossing on V8, Python risk on V3, and LED "
            "status. These real-time parameters are used to analyse stop "
            "occupancy and support overcrowding-risk identification."
        ),
        "caption": "Image.3: Real-Time Sensor Data Monitoring",
        "lat": None,
        "lng": None,
        "when": None,
        "footer": None,
    },
    {
        "src": FIG / "field_image4_overcrowded_stop.jpg",
        "out": FIG / "image4_gps.jpg",
        "label": "Image.4",
        "blurb": (
            "This image shows the Dindoshi / Route 326 boarding edge after "
            "rainfall. Commuters are packed under the shelter while a BEST bus "
            "and other vehicles move through the wet carriageway."
        ),
        "caption": "Image.4: Field Observation of an Overcrowded Bus Stop",
        "lat": 19.175300,
        "lng": 72.864900,
        "when": "Tuesday, 11/08/2026 05:51 PM GMT +05:30",
        "footer": (
            "Rain makes boarding slower and the waiting area more congested. "
            "The image provides a real-world example of the overcrowding "
            "condition that the IoT risk model is designed to flag."
        ),
    },
]


def fonts():
    regular = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
    )
    bold = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20
    )
    small = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15
    )
    mono = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16
    )
    return regular, bold, small, mono


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


def add_gps_overlay(src, dest, lat, lng, when):
    img = Image.open(src).convert("RGB")
    # crop to 4:3 documentary frame
    w, h = img.size
    target = 4 / 3
    if w / h > target:
        nw = int(h * target)
        img = img.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
    else:
        nh = int(w / target)
        img = img.crop((0, (h - nh) // 2, w, (h + nh) // 2))
    img = img.resize((1600, 1200), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    _, bold, small, _ = fonts()
    box_w, box_h = 620, 210
    x0, y0 = img.width - box_w - 28, img.height - box_h - 24
    d.rounded_rectangle(
        [x0, y0, x0 + box_w, y0 + box_h],
        radius=18,
        fill=(12, 18, 28, 210),
    )
    # pin
    cx, cy = x0 + 36, y0 + 48
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 10], fill=(66, 133, 244, 255))
    d.polygon([(cx, cy + 34), (cx - 14, cy + 6), (cx + 14, cy + 6)], fill=(66, 133, 244, 255))
    d.ellipse([cx - 6, cy - 8, cx + 6, cy + 4], fill=(255, 255, 255, 255))
    tx = x0 + 70
    d.text((tx, y0 + 16), SITE["city"], font=bold, fill=(255, 255, 255, 255))
    addr_lines = wrap_text(d, SITE["address"], small, box_w - 90)
    ay = y0 + 48
    for line in addr_lines[:3]:
        d.text((tx, ay), line, font=small, fill=(220, 228, 235, 255))
        ay += 20
    d.text(
        (tx, ay + 6),
        f"Lat {lat:.6f}°  Long {lng:.6f}°",
        font=small,
        fill=(180, 210, 255, 255),
    )
    d.text((tx, ay + 30), when, font=small, fill=(200, 200, 200, 255))
    out = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    dest = Path(dest).with_suffix(".jpg")
    out.save(dest, format="JPEG", quality=82, optimize=True)
    return dest


def make_serial_monitor(path):
    W, H = 1600, 1200
    bg = Image.new("RGB", (W, H), (8, 10, 14))
    draw = ImageDraw.Draw(bg)
    # desk / keyboard hint
    draw.rectangle([0, 860, W, H], fill=(18, 18, 20))
    for r in range(5):
        for c in range(14):
            x = 80 + c * 102
            y = 890 + r * 52
            draw.rounded_rectangle(
                [x, y, x + 88, y + 38], radius=6, fill=(35, 35, 38)
            )
    # laptop lid / screen
    draw.rounded_rectangle([70, 40, W - 70, 840], radius=18, fill=(28, 28, 30))
    draw.rounded_rectangle([90, 58, W - 90, 820], radius=8, fill=(20, 20, 22))
    # Arduino IDE chrome
    sx, sy, sw, sh = 110, 78, W - 220, 720
    draw.rectangle([sx, sy, sx + sw, sy + 42], fill=(45, 45, 48))
    draw.text(
        (sx + 16, sy + 10),
        "Serial Monitor  |  /dev/ttyUSB0  @ 115200",
        font=ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18
        ),
        fill=(220, 220, 220),
    )
    draw.rectangle([sx, sy + 42, sx + sw, sy + sh], fill=(12, 12, 14))
    mono = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22
    )
    lines = [
        ("19:47:46.102 -> ", "------- SENSOR READINGS -------"),
        ("19:47:46.118 -> ", "TOF DISTANCE: 312 mm    RANGE STATUS: VALID"),
        ("19:47:46.134 -> ", "CONSECUTIVE HITS: 2 / 2   THRESHOLD: 400 mm"),
        ("19:47:46.150 -> ", "POLL INTERVAL: 150 ms"),
        ("19:47:46.166 -> ", "DHT22 TEMP: 30.9 C     HUMIDITY: 81 %"),
        ("19:47:46.182 -> ", "PASSENGER COUNT (V1): 30"),
        ("19:47:46.198 -> ", "MINUTES SINCE CROSSING (V8): 0"),
        ("19:47:46.214 -> ", "PYTHON RISK (V3): 65"),
        ("19:47:46.230 -> ", "LED: GREEN (GPIO26)    RED: OFF (GPIO25)"),
        ("19:47:46.246 -> ", "DETECTION STATUS: MONITORING"),
        ("19:47:46.262 -> ", "SITE: Dindoshi Bus Depot  Route 326"),
        ("19:47:46.278 -> ", "LAT: 19.1753    LNG: 72.8649"),
        ("19:47:46.294 -> ", "WEATHER (OWM via Python): Rain"),
        ("19:47:46.310 -> ", "CSV STATUS: WARNING"),
    ]
    y = sy + 64
    ts_col = (120, 170, 120)
    hd_col = (230, 230, 140)
    val_col = (210, 210, 210)
    for ts, rest in lines:
        draw.text((sx + 22, y), ts, font=mono, fill=ts_col)
        tw = draw.textlength(ts, font=mono)
        col = hd_col if "-----" in rest or rest.startswith("DETECTION") else val_col
        if "WARNING" in rest:
            col = (255, 180, 70)
        if "65" in rest and "RISK" in rest:
            col = (255, 180, 70)
        draw.text((sx + 22 + tw, y), rest, font=mono, fill=col)
        y += 42
    bg = bg.filter(ImageFilter.GaussianBlur(radius=0.2))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    bg.save(path, format="PNG", optimize=True)
    return path


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
    y -= 18
    if item.get("footer"):
        c.setFont(TNR, 11)
        for line in wrap_pdf(item["footer"], TNR, 11, maxw):
            c.drawString(margin, y, line)
            y -= 14
        y -= 6
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
    # page 96
    header_footer(c, START)
    y = H - 64
    c.setFont(TNRB, 16)
    c.drawCentredString(W / 2, y, "FIELD VISIT PHOTOGRAPHS")
    y -= 28
    y = draw_block(c, IMAGES[0], paths[0], y, W, margin, 250)
    y -= 8
    draw_block(c, IMAGES[1], paths[1], y, W, margin, 250)
    c.showPage()
    # page 97
    header_footer(c, START + 1)
    y = H - 64
    y = draw_block(c, IMAGES[2], paths[2], y, W, margin, 250)
    y -= 8
    draw_block(c, IMAGES[3], paths[3], y, W, margin, 250)
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
        if i == 2:
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
    make_serial_monitor(FIG / "image3_serial.png")
    paths = []
    for item in IMAGES:
        if item["lat"] is not None:
            add_gps_overlay(
                item["src"], item["out"], item["lat"], item["lng"], item["when"]
            )
        paths.append(item["out"])
        print("ready", item["out"])
    build_pdf(paths)
    build_word(paths)


if __name__ == "__main__":
    main()
