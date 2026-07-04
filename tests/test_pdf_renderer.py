from pathlib import Path

from filinglens.ingestion.pdf_renderer import render_pdf


def test_render_pdf():

    pdf = "data/raw/TCS/FY2024/annual_report.pdf"

    output = "tests/output"

    render_pdf(pdf, output)

    assert Path(output).exists()
