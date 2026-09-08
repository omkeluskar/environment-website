#!/usr/bin/env python3
"""Cover, certificate, proposal, TOC — friend's NMFC black-book front matter."""
from pathlib import Path

from PIL import Image
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor, Twips
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path("/workspace/cep-iot-bus-stop")
FIG = ROOT / "figures/front_matter"
CH = ROOT / "chapters"
LOGO_COVER = FIG / "logo_p1_0_129x211.png"
LOGO_HEAD = FIG / "logo_p2_0_102x177.png"
LOGO_WORD = ROOT / "figures/questionnaires/nmfc_logo.png"

RED = HexColor("#C00000")
BLUE = HexColor("#2E5A9C")
ORANGE = HexColor("#E36C09")
TNR = "Times-Roman"
TNRB = "Times-Bold"
TNRU = "Times-Bold"

TITLE = (
    "IoT-Based Bus Stop System for Public Transport Overcrowding "
    "Prediction Using Machine Learning"
)
STUDENTS = "Mr. Om Keluskar and Mr. Jashith Agre"
SEAT_A, SEAT_B = "24TIT078", "24TIT011"
SEATS = f"{SEAT_A} and {SEAT_B}"
GUIDE = "Prof. George Thekkevilayil"
GUIDE_COVER = "Mr. George Thekkevilayil"
COORD = "Prof. Vaishali Mishra"
YEAR = "2026–2027"
YEAR_SHORT = "2026-27"

TOC = [
    (
        "CHAPTER 1: INTRODUCTION AND COMMUNITY CONTEXT",
        1,
        [
            ("1.1. Project Background", 1),
            ("1.2. Community Problem Identification", 2),
            ("1.3. Community Need Assessment", 3),
            ("1.4. Existing System Analysis", 4),
            ("1.5. Problem Statement", 5),
            ("1.6. Proposed Solution", 5),
            ("1.7. Aim and Objectives", 6),
            ("1.8. Scope of Project", 7),
            ("1.9. Limitations", 8),
            ("1.10. Major Modules", 8),
            ("1.11. Success Criteria", 9),
            ("1.12. Expected Outcomes", 10),
            ("1.13. Chapter Summary", 10),
        ],
    ),
    (
        "CHAPTER 2: SYSTEM ANALYSIS AND REQUIREMENT ANALYSIS",
        11,
        [
            ("2.1. Introduction", 11),
            ("2.2. Literature Review", 11),
            ("2.3. Comparative Analysis", 15),
            ("2.4. Research Gap Identification", 17),
            ("2.5. Requirement Gathering", 18),
            ("2.6. Stakeholder Analysis", 19),
            ("2.7. Functional Requirements", 20),
            ("2.8. Nonfunctional Requirements", 21),
            ("2.9. Feasibility Study", 22),
            ("2.10. Software Requirements", 23),
            ("2.11. Hardware Requirements", 24),
            ("2.12. Project Schedule", 25),
            ("2.13. Development Methodology", 26),
        ],
    ),
    (
        "CHAPTER 3: SYSTEM DESIGN",
        27,
        [
            ("3.1. System Architecture", 27),
            ("3.2. System Workflow", 28),
            ("3.3. Block Diagram", 29),
            ("3.4. Functional Flow Diagram", 29),
            ("3.5. Circuit Diagram", 30),
            ("3.6. Component Interconnection Diagram", 31),
            ("3.7. Hardware Module Design", 33),
            ("3.8. Data Flow & Processing Logic", 35),
            ("3.9. Database Design (if applicable)", 37),
            ("3.10. Dashboard/UI Design", 38),
            ("3.11. Technology Stack", 42),
            ("3.12. Safety & Security Considerations", 43),
            ("3.13. Chapter Summary", 45),
        ],
    ),
    (
        "CHAPTER 4: DEVELOPMENT AND IMPLEMENTATION",
        46,
        [
            ("4.1. Development Environment", 46),
            ("4.2. Implementation Approach", 46),
            ("4.3. Hardware Assembly", 48),
            ("4.4. Firmware Development", 51),
            ("4.5. Cloud / Blynk Integration", 56),
            ("4.6. Dashboard Development", 58),
            ("4.7. Module-wise Implementation", 59),
            ("4.8. Algorithms and Control Logic", 60),
            ("4.9. Safety Features Implemented", 61),
            ("4.10. Prototype Development", 62),
            ("4.11. Prototype Photos & Demonstration", 63),
        ],
    ),
    (
        "CHAPTER 5: TESTING, VALIDATION AND PERFORMANCE EVALUATION",
        66,
        [
            ("5.1. Testing Strategy", 66),
            ("5.2. Unit Testing", 66),
            ("5.3. Integration Testing", 68),
            ("5.4. System Testing", 70),
            ("5.5. User Acceptance Testing", 72),
            ("5.6. Performance Evaluation", 72),
            ("5.7. Security Testing", 74),
            ("5.8. Validation Metrics", 75),
            ("5.9. Test Cases", 77),
            ("5.10. Defects Identified and Corrections", 78),
            ("5.11. Chapter Summary", 79),
        ],
    ),
    (
        "CHAPTER 6: COMMUNITY DEPLOYMENT AND IMPACT ASSESSMENT",
        80,
        [
            ("6.1. Beneficiary Profile", 80),
            ("6.2. Community Engagement Activities", 80),
            ("6.3. Pilot Deployment", 81),
            ("6.4. User Training", 82),
            ("6.5. Feedback Collection", 83),
            ("6.6. Feedback Analysis", 83),
            ("6.7. Impact Assessment", 85),
            ("6.8. Outcome Achievement Matrix", 86),
            ("6.9. Sustainability Plan", 86),
        ],
    ),
    (
        "CHAPTER 7: RESULTS, DISCUSSION, CONCLUSION AND FUTURE SCOPE",
        87,
        [
            ("7.1. Results and Discussion", 87),
            ("7.2. Achievement of Objectives", 88),
            ("7.3. Project Contributions", 89),
            ("7.4. Limitations", 90),
            ("7.5. Future Enhancements", 90),
            ("7.6. Conclusion", 91),
        ],
    ),
]

BACK = [
    ("REFERENCES", "86"),
    ("APPENDIX A: SYSTEM LOGIC", "89"),
    ("SURVEY QUESTIONNAIRE", "94"),
    ("FEEDBACK QUESTIONNAIRE", "95"),
    ("FIELD VISIT PHOTOGRAPHS", "96"),
    ("ANNEXURES", "94 – 98"),
]


def border(c, inset=22):
    W, H = letter
    c.setStrokeColor(black)
    c.setLineWidth(1.0)
    c.rect(inset, inset, W - 2 * inset, H - 2 * inset)


def wrap(c, text, font, size, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def letterhead(c, y_top):
    """Friend's red/blue header with logo at left."""
    W, H = letter
    if LOGO_HEAD.exists():
        c.drawImage(
            str(LOGO_HEAD),
            40,
            y_top - 78,
            width=42,
            height=72,
            mask="auto",
            preserveAspectRatio=True,
        )
    c.setFillColor(RED)
    c.setFont(TNRB, 16)
    c.drawCentredString(W / 2, y_top - 8, "Nirmala Memorial Foundation College")
    c.drawCentredString(W / 2, y_top - 26, "of Commerce and Science")
    c.setFillColor(BLUE)
    c.setFont(TNRB, 12)
    c.drawCentredString(W / 2, y_top - 44, "(Autonomous)")
    c.setFont(TNR, 9)
    c.drawCentredString(
        W / 2,
        y_top - 58,
        "Re-Accredited by NAAC with B++ Grade & ISO 9001:2015 Certified",
    )
    c.drawCentredString(
        W / 2,
        y_top - 70,
        "Recognized under Section 2 (f) & 12 (B) of the UGC Act, 1956",
    )
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1.1)
    c.line(40, y_top - 84, W - 40, y_top - 84)
    c.setFillColor(BLUE)
    c.setFont(TNR, 8.5)
    c.drawCentredString(
        W / 2,
        y_top - 98,
        "D S Road, Asha Nagar, Thakur Complex, Kandivali (East), "
        "Mumbai-400101  Tel: 022-69436400",
    )
    c.line(40, y_top - 108, W - 40, y_top - 108)
    c.setFillColor(black)
    return y_top - 124


def draw_cover(c):
    W, H = letter
    border(c)
    y = H - 56
    c.setFillColor(black)
    c.setFont(TNRB, 13)
    for line in wrap(
        c,
        "NIRMALA MEMORIAL FOUNDATION COLLEGE OF COMMERCE AND SCIENCE",
        TNRB,
        13,
        W - 80,
    ):
        c.drawCentredString(W / 2, y, line)
        y -= 16
    c.setFont(TNRB, 12)
    c.drawCentredString(W / 2, y, "(AUTONOMOUS)")
    y -= 16
    c.setFont(TNR, 9)
    for line in wrap(
        c,
        "Re-Accredited by NAAC with B++ Grade & ISO 9001:2015 Certified "
        "Recognized under Section 2 (f) & 12 (B) of the UGC Act, 1956.",
        TNR,
        9,
        W - 90,
    ):
        c.drawCentredString(W / 2, y, line)
        y -= 12
    c.setFont(TNR, 10)
    c.drawCentredString(W / 2, y, "Kandivali (East), Mumbai-400101.")
    y -= 28
    if LOGO_COVER.exists():
        c.drawImage(
            str(LOGO_COVER),
            W / 2 - 38,
            y - 118,
            width=76,
            height=124,
            mask="auto",
            preserveAspectRatio=True,
        )
        y -= 140
    c.setFont(TNRB, 16)
    for line in wrap(c, TITLE, TNRB, 16, W - 90):
        c.drawCentredString(W / 2, y, line)
        y -= 20
    y -= 10
    c.setFont(TNRB, 13)
    c.drawCentredString(W / 2, y, "A Project Report")
    y -= 18
    c.setFont(TNR, 11)
    for line in wrap(
        c,
        "Submitted in partial fulfillment of the requirements "
        "For the degree of B.Sc. Information Technology aligned with "
        "the NEP-2020 Community Engagement Project (CEP)",
        TNR,
        11,
        W - 100,
    ):
        c.drawCentredString(W / 2, y, line)
        y -= 15
    y -= 12
    c.setFont(TNR, 12)
    c.drawCentredString(W / 2, y, "By")
    y -= 18
    c.setFont(TNRB, 13)
    c.drawCentredString(W / 2, y, STUDENTS)
    y -= 16
    c.setFont(TNR, 12)
    c.drawCentredString(W / 2, y, f"Seat No: {SEAT_A}, {SEAT_B}")
    y -= 15
    c.drawCentredString(W / 2, y, "Semester: V")
    y -= 28
    c.drawCentredString(W / 2, y, "Under the esteemed guidance of")
    y -= 18
    c.setFont(TNRB, 13)
    c.drawCentredString(W / 2, y, GUIDE_COVER)
    y -= 16
    c.drawCentredString(W / 2, y, "Assistant Professor")
    y -= 36
    c.setFont(TNRB, 12)
    c.drawCentredString(W / 2, y, "BACHELOR OF SCIENCE INFORMATION TECHNOLOGY")
    y -= 18
    c.drawCentredString(W / 2, y, f"Academic Year: {YEAR}")


def draw_certificate(c):
    W, H = letter
    border(c, 20)
    y = letterhead(c, H - 42)
    y -= 18
    c.setFont(TNRB, 16)
    c.drawCentredString(W / 2, y, "CERTIFICATE OF PROJECT")
    y -= 18
    c.drawCentredString(W / 2, y, "COMPLETION")
    c.setStrokeColor(black)
    c.setLineWidth(0.8)
    tw = stringWidth("CERTIFICATE OF PROJECT COMPLETION", TNRB, 16)
    # underline the two-line title block
    c.line(W / 2 - 160, y - 4, W / 2 + 160, y - 4)
    y -= 22
    c.setFont(TNRB, 13)
    c.drawCentredString(W / 2, y, "B.Sc. (Information Technology)")
    c.line(W / 2 - 120, y - 3, W / 2 + 120, y - 3)
    y -= 36
    body = (
        f'This is to certify that {STUDENTS}, students of T.Y.B.Sc. '
        f"(Information Technology), Semester V, bearing Seat No. {SEAT_A} and "
        f'{SEAT_B}, has successfully completed the Project Work titled "{TITLE}." '
        f"The project has been submitted in partial fulfillment of the requirements "
        f"prescribed in the syllabus for the award of the Degree of Bachelor of "
        f"Science in Information Technology for the academic year {YEAR}. The "
        f"practical and project work has been carried out successfully under the "
        f"supervision of the undersigned."
    )
    c.setFont(TNR, 12)
    for line in wrap(c, body, TNR, 12, W - 90):
        c.drawString(48, y, line)
        y -= 16
    y = 175
    xs = [70, W / 2, W - 70]
    labels = ["Internal Examiner", "External Examiner", "Co-ordinator"]
    names = [GUIDE, "", COORD]
    c.setStrokeColor(black)
    c.setLineWidth(1)
    for x, lab, name in zip(xs, labels, names):
        c.setFont(TNRB, 11)
        c.drawCentredString(x, y + 14, lab)
        c.line(x - 70, y, x + 70, y)
        if name:
            c.setFont(TNRB, 11)
            c.drawCentredString(x, y - 16, name)
    c.setFont(TNR, 11)
    c.drawCentredString(W / 2, 48, "College seal and Date")


def draw_proposal(c):
    W, H = letter
    border(c, 20)
    y = letterhead(c, H - 42)
    y -= 16
    c.setFont(TNRB, 14)
    c.drawCentredString(W / 2, y, "PROJECT PROPOSAL APPROVAL SHEET")
    c.setStrokeColor(black)
    c.setLineWidth(0.8)
    c.line(W / 2 - 155, y - 3, W / 2 + 155, y - 3)
    y -= 20
    c.setFont(TNRB, 12)
    c.drawCentredString(W / 2, y, "Department of Information Technology")
    y -= 16
    c.drawCentredString(W / 2, y, f"Academic Year {YEAR_SHORT}")
    y -= 36
    rows = [
        (f"1.  Name of the Students:  {STUDENTS}", False),
        (f"2.  Seat Number:  {SEAT_A}, {SEAT_B}", False),
        ("3.  Is this your first submission?     Yes            No", True),
        (f"4.  Name of the Guide:  {GUIDE}", False),
        ("5.  Teaching Experience of the Guide:  26 Years", False),
    ]
    c.setFont(TNR, 12)
    for text, boxes in rows:
        c.setFont(TNRB, 12)
        c.drawString(50, y, text)
        if boxes:
            c.setLineWidth(1)
            c.rect(318, y - 1, 11, 11, stroke=1, fill=0)
            c.rect(400, y - 1, 11, 11, stroke=1, fill=0)
        y -= 22
    y -= 18
    para = (
        f'The proposed project titled "{TITLE}." submitted by the above students, '
        f"has been examined and found suitable for the partial fulfilment of the "
        f"requirements for Semester V of the B.Sc IT Degree Programme. The project "
        f"is hereby approved for implementation under the guidance of the undersigned."
    )
    c.setFont(TNR, 12)
    for line in wrap(c, para, TNR, 12, W - 100):
        c.drawString(50, y, line)
        y -= 16
    y = 150
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.line(50, y, 230, y)
    c.line(W - 230, y, W - 50, y)
    c.setFont(TNR, 11)
    c.drawString(50, y - 16, "Signature of Guide")
    c.drawRightString(W - 50, y - 16, "Signature of Co-ordinator")
    c.drawString(50, y - 36, "Date:")
    c.drawRightString(W - 50, y - 36, "Date:")


def toc_line(c, left, right, y, text, page, bold=False, size=12):
    font = TNRB if bold else TNR
    c.setFont(font, size)
    num = str(page)
    nw = stringWidth(num, font, size)
    max_title = right - left - nw - 12
    # keep on one line; shrink if needed
    title = text
    while stringWidth(title, font, size) > max_title - 20 and len(title) > 20:
        title = title[:-2]
    tw = stringWidth(title, font, size)
    c.drawString(left, y, title)
    gap_x0 = left + tw + 4
    gap_x1 = right - nw - 4
    c.setFont(TNR, 10)
    x = gap_x0
    while x < gap_x1:
        c.drawString(x, y, ".")
        x += 4.2
    c.setFont(font, size)
    c.drawRightString(right, y, num)


def draw_toc_pages(c):
    W, H = letter
    left, right = 50, W - 50
    first = True

    def new_page():
        nonlocal first
        if not first:
            c.showPage()
        first = False
        border(c)
        return H - 52

    y = new_page()
    c.setFont(TNRB, 16)
    c.drawCentredString(W / 2, y, "TABLE OF CONTENTS")
    y -= 28
    for title, page, secs in TOC:
        if y < 90:
            y = new_page()
        toc_line(c, left, right, y, title, page, bold=True, size=11)
        y -= 16
        for s, sp in secs:
            if y < 70:
                y = new_page()
            toc_line(c, left + 12, right, y, s, sp, bold=False, size=12)
            y -= 14
        y -= 10
    if y < 70 + 16 * len(BACK):
        y = new_page()
    y -= 4
    for title, page in BACK:
        toc_line(c, left, right, y, title, page, bold=True, size=12)
        y -= 16


def build_pdfs():
    CH.mkdir(parents=True, exist_ok=True)
    cover = CH / "Cover_Page.pdf"
    c = canvas.Canvas(str(cover), pagesize=letter)
    draw_cover(c)
    c.save()
    cert = CH / "Certificate_of_Project_Completion.pdf"
    c = canvas.Canvas(str(cert), pagesize=letter)
    draw_certificate(c)
    c.save()
    prop = CH / "Project_Proposal_Approval_Sheet.pdf"
    c = canvas.Canvas(str(prop), pagesize=letter)
    draw_proposal(c)
    c.save()
    toc = CH / "Table_of_Contents.pdf"
    c = canvas.Canvas(str(toc), pagesize=letter)
    draw_toc_pages(c)
    c.save()
    # combined
    import pymupdf
    out = CH / "Front_Matter.pdf"
    merged = pymupdf.open()
    for p in (cover, cert, prop, toc):
        merged.insert_pdf(pymupdf.open(p))
    # append existing survey + feedback
    for extra in (
        CH / "CEP_Survey_Questionnaire.pdf",
        CH / "CEP_Feedback_Questionnaire.pdf",
    ):
        if extra.exists():
            merged.insert_pdf(pymupdf.open(extra))
    merged.save(out)
    print("wrote", cover, cert, prop, toc, out)


def set_run(run, *, size=12, bold=False, color=None, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def pfmt(p, align="center", before=0, after=6, line=16):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = Pt(line)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.alignment = {
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "both": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
    }[align]


def page_border(section):
    borders = OxmlElement("w:pgBorders")
    borders.set(qn("w:offsetFrom"), "page")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "12")
        el.set(qn("w:space"), "18")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    section._sectPr.append(borders)


def add_toc_para(doc, text, page, bold=False, indent=0):
    p = doc.add_paragraph()
    pfmt(p, align="left", before=1, after=1, line=16)
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    tab = p.paragraph_format.tab_stops.add_tab_stop
    tab(Cm(16.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    r = p.add_run(text)
    set_run(r, size=12, bold=bold)
    r2 = p.add_run("\t" + str(page))
    set_run(r2, size=12, bold=bold)


def build_word():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    sec.left_margin = Cm(2.2)
    sec.right_margin = Cm(2.2)
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.8)
    page_border(sec)

    # COVER
    for line, size, bold in [
        ("NIRMALA MEMORIAL FOUNDATION COLLEGE OF", 13, True),
        ("COMMERCE AND SCIENCE", 13, True),
        ("(AUTONOMOUS)", 12, True),
    ]:
        p = doc.add_paragraph()
        pfmt(p, after=2, line=16)
        set_run(p.add_run(line), size=size, bold=bold)
    p = doc.add_paragraph()
    pfmt(p, after=2, line=12)
    set_run(
        p.add_run(
            "Re-Accredited by NAAC with B++ Grade & ISO 9001:2015 Certified "
            "Recognized under Section 2 (f) & 12 (B) of the UGC Act, 1956."
        ),
        size=9,
    )
    p = doc.add_paragraph()
    pfmt(p, after=10, line=14)
    set_run(p.add_run("Kandivali (East), Mumbai-400101."), size=10)
    if LOGO_COVER.exists():
        p = doc.add_paragraph()
        pfmt(p, after=10)
        p.add_run().add_picture(str(LOGO_COVER), height=Cm(3.8))
    p = doc.add_paragraph()
    pfmt(p, after=10, line=20)
    set_run(p.add_run(TITLE), size=16, bold=True)
    p = doc.add_paragraph()
    pfmt(p, after=4)
    set_run(p.add_run("A Project Report"), size=13, bold=True)
    p = doc.add_paragraph()
    pfmt(p, after=10, line=16)
    set_run(
        p.add_run(
            "Submitted in partial fulfillment of the requirements for the degree of "
            "B.Sc. Information Technology aligned with the NEP-2020 Community "
            "Engagement Project (CEP)"
        ),
        size=11,
    )
    p = doc.add_paragraph()
    pfmt(p, after=2)
    set_run(p.add_run("By"), size=12)
    p = doc.add_paragraph()
    pfmt(p, after=2)
    set_run(p.add_run(STUDENTS), size=13, bold=True)
    p = doc.add_paragraph()
    pfmt(p, after=2)
    set_run(p.add_run(f"Seat No: {SEAT_A}, {SEAT_B}"), size=12)
    p = doc.add_paragraph()
    pfmt(p, after=10)
    set_run(p.add_run("Semester: V"), size=12)
    p = doc.add_paragraph()
    pfmt(p, after=2)
    set_run(p.add_run("Under the esteemed guidance of"), size=12)
    p = doc.add_paragraph()
    pfmt(p, after=2)
    set_run(p.add_run(GUIDE_COVER), size=13, bold=True)
    p = doc.add_paragraph()
    pfmt(p, after=14)
    set_run(p.add_run("Assistant Professor"), size=13, bold=True)
    p = doc.add_paragraph()
    pfmt(p, after=4)
    set_run(p.add_run("BACHELOR OF SCIENCE INFORMATION TECHNOLOGY"), size=12, bold=True)
    p = doc.add_paragraph()
    pfmt(p, after=0)
    set_run(p.add_run(f"Academic Year: {YEAR}"), size=12, bold=True)

    doc.add_page_break()
    # CERT
    p = doc.add_paragraph()
    pfmt(p, after=2, line=18)
    set_run(p.add_run("CERTIFICATE OF PROJECT COMPLETION"), size=16, bold=True)
    p = doc.add_paragraph()
    pfmt(p, after=12)
    set_run(p.add_run("B.Sc. (Information Technology)"), size=13, bold=True)
    p = doc.add_paragraph()
    pfmt(p, align="both", after=20, line=18)
    set_run(
        p.add_run(
            f"This is to certify that {STUDENTS}, students of T.Y.B.Sc. "
            f"(Information Technology), Semester V, bearing Seat No. {SEAT_A} and "
            f'{SEAT_B}, has successfully completed the Project Work titled "{TITLE}." '
            f"The project has been submitted in partial fulfillment of the requirements "
            f"prescribed in the syllabus for the award of the Degree of Bachelor of "
            f"Science in Information Technology for the academic year {YEAR}. The "
            f"practical and project work has been carried out successfully under the "
            f"supervision of the undersigned."
        ),
        size=12,
    )
    p = doc.add_paragraph()
    pfmt(p, after=20, line=16)
    set_run(
        p.add_run(
            f"Internal Examiner                    External Examiner                    Co-ordinator\n"
            f"{GUIDE}                                                                      {COORD}"
        ),
        size=11,
        bold=True,
    )
    p = doc.add_paragraph()
    pfmt(p)
    set_run(p.add_run("College seal and Date"), size=11)

    doc.add_page_break()
    # PROPOSAL
    p = doc.add_paragraph()
    pfmt(p, after=4)
    set_run(p.add_run("PROJECT PROPOSAL APPROVAL SHEET"), size=14, bold=True)
    p = doc.add_paragraph()
    pfmt(p, after=2)
    set_run(p.add_run("Department of Information Technology"), size=12, bold=True)
    p = doc.add_paragraph()
    pfmt(p, after=14)
    set_run(p.add_run(f"Academic Year {YEAR_SHORT}"), size=12, bold=True)
    for line in [
        f"1.  Name of the Students:  {STUDENTS}",
        f"2.  Seat Number:  {SEAT_A}, {SEAT_B}",
        "3.  Is this your first submission?     Yes  ☐     No  ☐",
        f"4.  Name of the Guide:  {GUIDE}",
        "5.  Teaching Experience of the Guide:  26 Years",
    ]:
        p = doc.add_paragraph()
        pfmt(p, align="left", after=6, line=16)
        set_run(p.add_run(line), size=12, bold=True)
    p = doc.add_paragraph()
    pfmt(p, align="both", before=10, after=20, line=18)
    set_run(
        p.add_run(
            f'The proposed project titled "{TITLE}." submitted by the above students, '
            f"has been examined and found suitable for the partial fulfilment of the "
            f"requirements for Semester V of the B.Sc IT Degree Programme. The project "
            f"is hereby approved for implementation under the guidance of the undersigned."
        ),
        size=12,
    )
    p = doc.add_paragraph()
    pfmt(p, align="left", after=4)
    set_run(p.add_run("Signature of Guide                          Signature of Co-ordinator"), size=11)
    p = doc.add_paragraph()
    pfmt(p, align="left")
    set_run(p.add_run("Date:                                                Date:"), size=11)

    doc.add_page_break()
    p = doc.add_paragraph()
    pfmt(p, after=12)
    set_run(p.add_run("TABLE OF CONTENTS"), size=16, bold=True)
    for title, page, secs in TOC:
        add_toc_para(doc, title, page, bold=True)
        for s, sp in secs:
            add_toc_para(doc, s, sp, indent=0.6)
    for title, page in BACK:
        add_toc_para(doc, title, page, bold=True)

    out = CH / "Front_Matter.docx"
    doc.save(out)
    print("wrote", out)


if __name__ == "__main__":
    build_pdfs()
    build_word()
