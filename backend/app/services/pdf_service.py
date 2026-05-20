"""
PDF report generation service using ReportLab Platypus.
Indian government-styled validation reports.
"""
import io
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    HRFlowable,
)


# ─── Indian Government colour palette ────────────────────────
SAFFRON = colors.HexColor("#FF9933")
NAVY = colors.HexColor("#000080")
GREEN = colors.HexColor("#138808")
WHITE = colors.white
LIGHT_GREY = colors.HexColor("#F0F0F0")


def _build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "GovTitle",
        parent=styles["Title"],
        fontSize=18,
        textColor=NAVY,
        spaceAfter=6,
        alignment=1,
    ))
    styles.add(ParagraphStyle(
        "GovSubtitle",
        parent=styles["Normal"],
        fontSize=12,
        textColor=NAVY,
        spaceAfter=12,
        alignment=1,
    ))
    styles.add(ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "FieldLabel",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.grey,
    ))
    styles.add(ParagraphStyle(
        "FieldValue",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.black,
        spaceBefore=2,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "StatusPass",
        parent=styles["Normal"],
        fontSize=14,
        textColor=GREEN,
        alignment=1,
        spaceBefore=12,
    ))
    styles.add(ParagraphStyle(
        "StatusFail",
        parent=styles["Normal"],
        fontSize=14,
        textColor=colors.red,
        alignment=1,
        spaceBefore=12,
    ))
    return styles


def generate_validation_report(
    farmer: dict,
    scheme: dict,
    application: dict,
    validation_history: list,
) -> bytes:
    """Generate a PDF validation report and return the bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )
    styles = _build_styles()
    elements = []

    # ── Saffron header bar ───────────────────────────────────
    elements.append(HRFlowable(
        width="100%", thickness=4, color=SAFFRON, spaceAfter=8,
    ))

    # ── Title ────────────────────────────────────────────────
    elements.append(Paragraph("PashuRakshak", styles["GovTitle"]))
    elements.append(Paragraph(
        "Smart Livestock Verification &amp; Government Grant Monitoring System",
        styles["GovSubtitle"],
    ))
    elements.append(Paragraph("Validation Report", styles["GovSubtitle"]))
    elements.append(HRFlowable(
        width="100%", thickness=2, color=NAVY, spaceAfter=12,
    ))

    # ── Farmer Details ───────────────────────────────────────
    elements.append(Paragraph("Farmer Details", styles["SectionHeader"]))
    farmer_data = [
        ["Name", farmer.get("name", "N/A")],
        ["Mobile", farmer.get("mobile", "N/A")],
        ["Location", f"{farmer.get('city', 'N/A')}, {farmer.get('state', 'N/A')}"],
        ["Cattle Count", str(farmer.get("cattle_count", "N/A"))],
        ["Land (acres)", str(farmer.get("land_acres", "N/A"))],
    ]
    t = Table(farmer_data, colWidths=[2.5 * inch, 4 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_GREY),
        ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # ── Scheme Details ───────────────────────────────────────
    elements.append(Paragraph("Scheme Details", styles["SectionHeader"]))
    scheme_data = [
        ["Scheme Name", scheme.get("name", "N/A")],
        ["Sponsor", scheme.get("sponsor", "N/A")],
        ["Min Cattle Required", str(scheme.get("min_cattle", "N/A"))],
        ["Validations Required", str(scheme.get("validations_required", "N/A"))],
    ]
    t2 = Table(scheme_data, colWidths=[2.5 * inch, 4 * inch])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_GREY),
        ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 12))

    # ── Application Status ───────────────────────────────────
    status = application.get("status", "pending")
    elements.append(Paragraph("Application Status", styles["SectionHeader"]))
    status_style = "StatusPass" if status == "approved" else "StatusFail"
    elements.append(Paragraph(f"Status: {status.upper()}", styles[status_style]))
    elements.append(Spacer(1, 12))

    # ── Validation History Table ─────────────────────────────
    if validation_history:
        elements.append(Paragraph("Validation History", styles["SectionHeader"]))
        header = ["#", "Date", "Officer", "Action", "Notes"]
        rows = [header]
        for idx, v in enumerate(validation_history, 1):
            date_str = v.get("date", "N/A")
            if isinstance(date_str, datetime):
                date_str = date_str.strftime("%d-%b-%Y %H:%M")
            rows.append([
                str(idx),
                str(date_str),
                v.get("officer_name", "N/A"),
                v.get("action", "N/A"),
                v.get("notes", "-"),
            ])
        t3 = Table(rows, colWidths=[0.5 * inch, 1.5 * inch, 1.5 * inch, 1.2 * inch, 2 * inch])
        t3.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(t3)
    else:
        elements.append(Paragraph("No validation history available.", styles["FieldValue"]))

    elements.append(Spacer(1, 20))

    # ── Footer ───────────────────────────────────────────────
    elements.append(HRFlowable(width="100%", thickness=1, color=SAFFRON, spaceAfter=6))
    now_str = datetime.now(timezone.utc).strftime("%d-%b-%Y %H:%M UTC")
    elements.append(Paragraph(
        f"Generated on {now_str} | PashuRakshak – Government of India Initiative",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, textColor=colors.grey, alignment=1),
    ))

    # Build PDF
    doc.build(elements)
    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes
