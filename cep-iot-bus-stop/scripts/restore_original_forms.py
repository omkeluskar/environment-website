#!/usr/bin/env python3
"""Copy certificate and questionnaire pages from the original college PDF.
Do not redraw, strip, or restyle anything."""
from pathlib import Path

import pymupdf
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

ROOT = Path("/workspace/cep-iot-bus-stop")
SRC = ROOT / "figures/front_matter/source_forms.pdf"
CH = ROOT / "chapters"
TMP = Path("/tmp/cep_form_pages")

# 0-based page indexes in source_forms.pdf (the original 5-page pack)
PAGES = {
    "Certificate_of_Project_Completion": 1,
    "CEP_Survey_Questionnaire": 3,
    "CEP_Feedback_Questionnaire": 4,
}


def extract_page(src, index, dest):
    one = pymupdf.open()
    one.insert_pdf(src, from_page=index, to_page=index)
    dest.parent.mkdir(parents=True, exist_ok=True)
    one.save(dest, deflate=False, garbage=0)
    one.close()
    print("wrote", dest)


def pdf_to_word(pdf_path, docx_path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Inches(0))
    pdf = pymupdf.open(pdf_path)
    TMP.mkdir(parents=True, exist_ok=True)
    pix = pdf[0].get_pixmap(matrix=pymupdf.Matrix(300 / 72, 300 / 72), alpha=False)
    png = TMP / f"{pdf_path.stem}.png"
    pix.save(png)
    pdf.close()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    p.add_run().add_picture(str(png), width=Inches(8.5), height=Inches(11))
    doc.save(docx_path)
    print("wrote", docx_path)


def merge_front_matter():
    out = CH / "Front_Matter.pdf"
    merged = pymupdf.open()
    for p in (
        CH / "Cover_Page.pdf",
        CH / "Certificate_of_Project_Completion.pdf",
        CH / "Project_Proposal_Approval_Sheet.pdf",
        CH / "Table_of_Contents.pdf",
        CH / "CEP_Survey_Questionnaire.pdf",
        CH / "CEP_Feedback_Questionnaire.pdf",
    ):
        if p.exists():
            merged.insert_pdf(pymupdf.open(p))
    merged.save(out, garbage=0)
    print("wrote", out)


def main():
    src = pymupdf.open(SRC)
    for name, idx in PAGES.items():
        pdf = CH / f"{name}.pdf"
        extract_page(src, idx, pdf)
        pdf_to_word(pdf, CH / f"{name}.docx")
    src.close()
    merge_front_matter()


if __name__ == "__main__":
    main()
