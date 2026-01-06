from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph

import re
import json
import sys
from reportlab.lib.styles import ParagraphStyle
styles = getSampleStyleSheet()


# Load data from external JSON file
def load_data(json_path: str) -> dict:
    """Load report data from an external JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Default JSON file path
# Handle Jupyter/Code Interpreter environment where sys.argv contains kernel flags
json_file = "Reference_Adjudicator_Data.json"
if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
    json_file = sys.argv[1]

data = load_data(json_file)

# Create PDF
pdf_file = "Reference_Adjudicator_Report.pdf"
doc = SimpleDocTemplate(
    pdf_file,
    pagesize=landscape(letter),
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()
elements = []

styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["Normal"],
        fontSize=8,
        leading=10
    )
)

# --- Link helpers ------------------------------------------------------------

DOI_PATTERN = re.compile(r"(doi:\s*)(10\.\d{4,9}/[^\s]+)", re.IGNORECASE)

def make_doi_clickable(original_ref: str) -> str:
    """
    Replace 'doi:10.xxxx/yyy' with a fully blue clickable doi.org link,
    including the 'doi:' prefix.
    """
    def repl(m):
        doi = m.group(2).rstrip(".,;")  # trim trailing punctuation
        url = f"https://doi.org/{doi}"
        return f'<font color="blue"><u><a href="{url}">doi:{doi}</a></u></font>'

    return DOI_PATTERN.sub(repl, original_ref)



def pubmed_cell(pubmed_value: str) -> str:
    """
    If pubmed_value is a URL, render anchored blue link text.
    Otherwise, return as plain text.
    """
    if isinstance(pubmed_value, str) and pubmed_value.startswith("http"):
        return f'<font color="blue"><u><a href="{pubmed_value}">PubMed Title + First Author Search</a></u></font>'
    return pubmed_value


# Title
elements.append(Paragraph(data["report_title"], styles["Title"]))
elements.append(Spacer(1, 12))

# Summary
summary_text = (
    f"Total references checked: {data['summary_metrics']['total_references_checked']}<br/>"
    f"Verified matches: {data['summary_metrics']['verified_matches']}<br/>"
    f"Failed verifications: {data['summary_metrics']['failed_verifications']}<br/>"
    f"Failure rate: {data['summary_metrics']['failure_rate_percent']}%"
)
elements.append(Paragraph(summary_text, styles["Normal"]))
elements.append(Spacer(1, 12))

# Table data (4 columns only)
table_data = [
    ["Ref #", "Original Reference", "Verification Outcome", "PubMed Search"]
]

for row in data["rows"]:
    original_ref_html = make_doi_clickable(row["original_reference"])
    pubmed_html = pubmed_cell(row["pubmed_search"])

    table_data.append([
        Paragraph(row["ref_number"], styles["Normal"]),
        Paragraph(original_ref_html, styles["Normal"]),
        Paragraph(row["verification_outcome"], styles["Normal"]),
        Paragraph(pubmed_html, styles["Normal"])
    ])



# Column width ratios: 5% / 55% / 20% / 20%
total_width = landscape(letter)[0] - 72
col_widths = [
    total_width * 0.05,
    total_width * 0.55,
    total_width * 0.20,
    total_width * 0.20
]

table = Table(table_data, colWidths=col_widths, repeatRows=1)
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
    ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("FONT", (0,0), (-1,0), "Helvetica-Bold"),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))

elements.append(table)
elements.append(Spacer(1, 18))

# --- Appendix (optional) -----------------------------------------------------

if "appendix" in data and data["appendix"]:
    from reportlab.platypus import PageBreak
    
    # Add appendix style for body text
    styles.add(
        ParagraphStyle(
            name="AppendixBody",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            spaceAfter=12
        )
    )
    
    styles.add(
        ParagraphStyle(
            name="AppendixRefHeader",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            fontName="Helvetica-Bold",
            spaceAfter=6,
            spaceBefore=12
        )
    )
    
    elements.append(PageBreak())
    elements.append(Paragraph("Appendix: Detailed Verification Rationale", styles["Heading1"]))
    elements.append(Spacer(1, 12))
    
    for entry in data["appendix"]:
        # Reference header (e.g., "Reference 3: Smith et al. (2021)")
        ref_header = f"Reference {entry['ref_number']}: {entry.get('short_title', '')}"
        elements.append(Paragraph(ref_header, styles["AppendixRefHeader"]))
        
        # Rationale text (may contain multiple paragraphs separated by \n\n)
        rationale_text = entry.get("rationale", "")
        paragraphs = rationale_text.split("\n\n")
        for para in paragraphs:
            if para.strip():
                # Replace single newlines with <br/> for line breaks within paragraphs
                para_html = para.strip().replace("\n", "<br/>")
                elements.append(Paragraph(para_html, styles["AppendixBody"]))
        
        elements.append(Spacer(1, 6))

elements.append(Spacer(1, 18))

# Disclaimer
from datetime import datetime, timezone
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

disclaimer = (
    f"Disclaimer: Generated by Reference Adjudicator (custom GPT) "
    f"https://chatgpt.com/g/g-6953b9a21adc8191891811d34f34bf79-reference-adjudicator. "
    f"This report generated on {timestamp}. "
    "This report uses a structured, web-assisted workflow implemented by a probabilistic LLM. "
    "Results must be independently verified. No warranty (express or implied); use at own risk."
)


elements.append(Paragraph(disclaimer, styles["Small"]))

doc.build(elements)

print(f"PDF generated: {pdf_file}")
