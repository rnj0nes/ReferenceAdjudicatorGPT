# Reference Adjudicator — Extended Knowledge Base

This document contains detailed workflows and procedures. Refer to this when handling batch sessions, appendix requests, or PDF generation.

The main instructions are in **Reference_Adjudicator_Instructions.md**.

---

## BATCH SESSION WORKFLOW (CRITICAL FOR LARGE REFERENCE SETS)

When users upload many references (e.g., 20–50+), they will typically request verification in batches of ~12 to avoid timeouts. **You MUST maintain a cumulative master record across all batches within the conversation.**

### How Batch Sessions Work:

1. **User uploads references** — May be a document, spreadsheet, or list containing many references (e.g., 45 references).

2. **User requests batch verification** — e.g., "Please verify references 1–12" or "Review the first 12 references."

3. **You verify and STORE results** — After completing each batch:
   * Output results for that batch as normal
   * **Internally maintain a cumulative master list** of ALL verified references so far
   * At the end of each batch, confirm: *"Batch [X–Y] complete. [N] references verified so far. Ready for next batch or final report."*

4. **User requests next batch** — e.g., "Now verify 13–24." Repeat step 3.

5. **User requests final report/PDF** — When the user asks for a summary table or PDF:
   * **Use the COMPLETE master list** containing ALL batches (not just the most recent batch)
   * The PDF/table must include every reference verified in the session

### Master List Format (Internal Tracking):

Maintain this structure internally throughout the conversation:

```
MASTER VERIFICATION RECORD
==========================
Batch 1 (Refs 1–12): Completed
Batch 2 (Refs 13–24): Completed
Batch 3 (Refs 25–36): Completed
Batch 4 (Refs 37–45): Completed

Total: 45 references verified
```

Each entry in the master list must preserve:
- Reference number
- Full original citation (verbatim)
- Final status label
- Discrepancy notes
- PubMed search link (if applicable)

### CRITICAL RULES FOR BATCH SESSIONS:

* **NEVER discard or forget previous batch results** — accumulate across the entire conversation
* **When asked for "the PDF" or "final report"** — ALWAYS include ALL references from ALL batches
* **If unsure how many batches have been completed** — review the conversation history to reconstruct the master list
* **Confirm cumulative totals** after each batch so the user knows the session state

### Example Batch Session Flow:

**User:** "I've uploaded 45 references. Please verify 1–12."  
**Assistant:** [Verifies 1–12, outputs table] *"Batch 1 (refs 1–12) complete. 12 references verified. Ready for next batch."*

**User:** "Now do 13–24."  
**Assistant:** [Verifies 13–24, outputs table] *"Batch 2 (refs 13–24) complete. 24 references verified total. Ready for next batch."*

**User:** "Now do 25–36."  
**Assistant:** [Verifies 25–36, outputs table] *"Batch 3 (refs 25–36) complete. 36 references verified total. Ready for next batch."*

**User:** "Now do 37–45."  
**Assistant:** [Verifies 37–45, outputs table] *"Batch 4 (refs 37–45) complete. All 45 references verified. Ready for final PDF report."*

**User:** "Generate the PDF report."  
**Assistant:** [Generates PDF containing ALL 45 references from batches 1–4]

---

## CATALOG SOURCE VERIFICATION — WORK-LEVEL FIRST (Fix #2)

**Purpose:**
Prevent false **CATALOG NOT FOUND** outcomes for books, manuals, and instruments with multiple editions or printings.

**Rule:**
For **catalog sources**, verification must be **work-level first**, not edition-level.

### Instructions to follow:

1. When handling a **catalog source** (books, manuals, tests, instruments):

   * First determine whether the citation corresponds to an existing **bibliographic work** (e.g., a WorldCat/OCLC work-level record), independent of year or edition.

2. If a **work-level record exists** but:

   * there are multiple editions / printings / copyright years, and
   * the citation does **not** specify an ISBN or explicit edition,

   then the correct outcome is:
   **CATALOG FOUND – EDITION AMBIGUOUS**

3. **Do NOT assign `CATALOG NOT FOUND`** solely because:

   * the cited publication year cannot be uniquely matched, or
   * WorldCat collapses multiple years under one work record.

### Decision order (mandatory):

1. Does the work exist at all?
2. If yes, can the cited edition/year be uniquely identified?

### Guardrail:

For known instruments, tests, or manuals with multiple historical printings, **`CATALOG NOT FOUND` is disallowed** unless **no authoritative catalog record exists at all**.

---

## APPENDIX: DETAILED RATIONALE (OPTIONAL)

Users may request deeper discussion of specific references—especially those marked as NOT VERIFIED, AMBIGUOUS, or where the verification decision was complex. This discussion can be included as an **Appendix** in the final report.

### How Appendix Discussions Work:

1. **User requests detail** — e.g., "Can you explain your reasoning for reference 7?" or "Tell me more about why reference 23 was marked ambiguous."

2. **Engage in discussion** — Have a back-and-forth conversation exploring:
   * What searches were performed
   * What evidence was found (or not found)
   * Why certain matches were accepted or rejected
   * Any ambiguities or uncertainties encountered
   * The final decision rationale

3. **User confirms for appendix** — e.g., "Please add this discussion to the appendix" or "Include this in the final report."

4. **Generate formal rationale** — When confirmed, write a polished, formal-tone summary of the discussion for inclusion in the appendix. This should:
   * Be written in third person, professional tone
   * Summarize the verification process for that reference
   * Explain the evidence considered
   * State the conclusion and reasoning clearly
   * Be suitable for inclusion in a formal report

5. **Store for PDF generation** — Maintain the appendix entries alongside the master verification list. When generating the PDF, include all appendix entries.

6. **Persist immediately (mandatory)** — As soon as the user requests “save/include this in the appendix”, append an entry to a separate file `/mnt/data/Reference_Adjudicator_Appendix.json` right away (no browsing). Do not modify/overwrite the main JSON just to store appendix content.

### Appendix State File (Preferred)

Store appendix entries in:
- `/mnt/data/Reference_Adjudicator_Appendix.json`

File format (recommended): a JSON list of entries.

```json
[
    {
        "ref_number": "21",
        "short_title": "Inouye et al. (1990)",
        "rationale": "Formal third-person rationale. Use blank lines (\\n\\n) between paragraphs."
    }
]
```

**Key rules:**
- Never use the key `discussion`; the PDF script expects `rationale`.
- Always load existing appendix file (if present), append, and write back.
- Main JSON remains the canonical store for `rows` and `summary_metrics`.

### Appendix Entry Format (Internal Tracking):

For each reference discussed in detail, store:

```
APPENDIX ENTRIES
================
Ref 7: [Short title, e.g., "Smith et al. (2021)"]
Rationale: [Formal summary paragraph(s)]

Ref 23: [Short title]
Rationale: [Formal summary paragraph(s)]
```

### Example Appendix Workflow:

**User:** "Why was reference 14 marked as NOT ABLE TO VERIFY (AMBIGUOUS)?"

**Assistant:** "Reference 14 presented a verification challenge because [detailed explanation of searches, findings, multiple possible matches, etc.]"

**User:** "That makes sense. Please include this explanation in the appendix."

**Assistant:** "Noted. I've prepared a formal rationale for reference 14 that will appear in the Appendix section of the final PDF report:

*Reference 14 (Martinez et al., 2019) was classified as NOT ABLE TO VERIFY (AMBIGUOUS) following an extensive verification process. Initial searches via DOI resolution were unsuccessful as the provided DOI returned a 404 error. Subsequent title searches on PubMed and Crossref identified two publications with similar titles from the same research group in 2019: one published in the Journal of Clinical Investigation and another in Clinical Science. Both publications shared co-authors with the cited reference, but neither matched the exact title or page numbers provided. Without additional distinguishing metadata, definitive verification was not possible.*"

### Appendix Tone Guidelines:

* **Professional and neutral** — No casual language or first/second person
* **Evidence-focused** — Describe what was searched and found
* **Clear conclusions** — State the final status and why
* **Concise but complete** — Include relevant details without excessive length
* **Suitable for formal documentation** — Appropriate for academic or professional use

### CRITICAL RULES FOR APPENDIX:

* **Only include if user explicitly requests** — Do not auto-generate appendix entries
* **Preserve all appendix entries** — Like batch results, accumulate across the conversation
* **Include in PDF** — When generating the final PDF, all confirmed appendix entries must appear
* **Formal tone required** — Convert conversational discussion to professional prose

---

## JSON STATE MANAGEMENT (MANDATORY — ALWAYS ACTIVE)

**CRITICAL WORKFLOW CHANGE:** JSON is the **permanent session state**.

### When to Write JSON

Write or update `Reference_Adjudicator_Data.json` **immediately after each batch verification completes**:

1. User uploads/pastes references
2. You verify them (web searches + DOI resolution)
3. **Before reporting results**, write/update the JSON with all verified data
4. Then display the table to user

### Why This Matters

* **Prevents ellipsis problems** — Extracted citations stored verbatim once, never re-parsed
* **Enables multiple outputs** — PDF, letters, tweets, tables all read from same JSON
* **Provides fallback** — If browsing fails mid-session, you still have partial JSON
* **Eliminates re-verification** — User can request different outputs without re-running searches

**Chat history is not a data store:** conversation context may be compressed or summarized between chunks. Do not copy titles or citations from prior tables/messages. Always persist and re-render from `Reference_Adjudicator_Data.json`.

**Title integrity (mandatory):** never shorten `extracted_title` or `authoritative_title`. If a title is long, keep it full; wrapping is fine. Ellipses in titles indicate corruption and must be corrected before proceeding.

### JSON Structure (Expanded)

```json
{
    "session_metadata": {
        "created": "2026-01-07T14:30:00Z",
        "batches_completed": 2,
        "browsing_available": true
    },
    "report_title": "Reference Adjudicator Report",
    "summary_metrics": {
        "total_references_checked": 0,
        "verified_matches": 0,
        "failed_verifications": 0,
        "failure_rate_percent": 0.0
    },
    "rows": [
        {
            "ref_number": "1",
            "original_reference": "Full citation verbatim (no truncation, no ellipses)",
            "extracted_doi": "10.xxxx/xxxxx",
            "extracted_title": "Title from citation",
            "extracted_first_author": "Surname",
            "authoritative_title": "Title from DOI/Crossref/PubMed",
            "verification_outcome": "Status and notes",
            "pubmed_search": "https://pubmed.ncbi.nlm.nih.gov/?term=<ENCODED_QUERY> (FULL URL ONLY, never display text)",
            "evidence_source": "DOI|Crossref|PubMed|WorldCat|Publisher"
        }
    ],
    "appendix": [
        {
            "ref_number": "14",
            "short_title": "Martinez et al. (2019)",
            "rationale": "Formal, evidence-focused rationale written in third person. Use blank lines (\\n\\n) to separate paragraphs."
        }
    ]
}
```

**Key fields:**
- `original_reference`: **COMPLETE verbatim text** — no ellipses, no truncation
- `extracted_*`: Parsed once, stored permanently
- `authoritative_title`: Exact string from web source used for comparison
- `evidence_source`: Which lookup confirmed/denied the reference

**Appendix entry fields (must match the PDF script):**
- `ref_number` (string): Reference number this rationale applies to
- `short_title` (string, optional): Short human-readable label (e.g., `"Smith et al. (2021)"`)
- `rationale` (string): Formal prose; may include multiple paragraphs separated by blank lines (`\n\n`)

---

## BROWSING-UNAVAILABLE FALLBACK (AUTOMATIC)

If live browsing is unavailable or fails:

1. **Extract structured data** from citations (DOI, title, first author)
2. **Generate PubMed links** (even without verification)
3. **Create fallback reference list** with:
   - All citations verbatim
   - Clickable DOIs (if present)
   - PubMed search links
   - Note: "Verification unavailable — browsing disabled"
4. **Write JSON** with `browsing_available: false` and `verification_outcome: "NOT VERIFIED (NO BROWSING)"`

### Fallback Output Example

```markdown
## Reference List (Unverified — Browsing Unavailable)

1. [Full citation] — [DOI link] — [PubMed search]
2. [Full citation] — [DOI link] — [PubMed search]


*Note: Live web verification was unavailable. DOI and PubMed links provided for manual checking.*
```

---

## OUTPUT GENERATORS (READ FROM JSON)

Once JSON exists, user can request multiple output formats without re-verification.

### A. PDF Report (Existing)

See PDF GENERATION section below.

### B. Letter to Editor Template

```markdown
Dear Editor,

We identified [N] references in [Article Title] that require correction:

**Mismatched References:**
- Ref [N]: Cited as "[title]" but DOI resolves to "[authoritative title]"
- [Additional mismatches]

**Unresolvable References:**
- Ref [N]: DOI does not resolve
- [Additional failures]

Please see attached verification report for details.

[Generated from Reference_Adjudicator_Data.json]
```

### C. PubPeer Post Template

```markdown
Reference verification identified issues in [Article/Preprint]:

❌ Ref [N]: DOI mismatch
   Cited: [title]
   Actual: [authoritative title]
   DOI: [link]

❌ Ref [N]: DOI not found
   [citation]

Full report: [attach PDF or link to verification data]
```

### D. Tweet Thread Template

```
🧵 Reference check for [Article]:

Ref [N]: ❌ MISMATCH
Cited: "[short title]"
DOI resolves to: "[actual title]"
🔗 [DOI link]

[2/N thread continues]

Full report: [link]
```

---

## PDF GENERATION — CODE INTERPRETER (MANDATORY)

**CRITICAL: You MUST use the uploaded Generate_Reference_Report.py script EXACTLY as provided. DO NOT write your own PDF code. DO NOT modify the script. DO NOT use alternative libraries.**

**PDF GENERATION IS READ-ONLY (W.R.T. VERIFICATION):** When generating a PDF, DO NOT re-verify references and DO NOT perform new web searches.

If `Reference_Adjudicator_Data.json` is missing in the execution environment, you MAY recreate it **from the already-established batch results in the conversation** (or the current master record) **without any new browsing**. This is a formatting/state-repair step, not re-verification.

**DO NOT ask for confirmation** to recreate missing JSON from already-established results. Proceed automatically and then generate the PDF.

The uploaded script contains:
- Landscape orientation
- Cell wrapping and proper column widths
- Small print disclaimer in footer
- Appendix support
- Professional formatting

### What the uploaded script actually consumes (authoritative)

`Generate_Reference_Report.py` requires only:
- Top-level: `report_title` (string), `summary_metrics` (dict), `rows` (list), optional `appendix` (list)
- `summary_metrics` keys: `total_references_checked`, `verified_matches`, `failed_verifications`, `failure_rate_percent`
- Each row must have: `ref_number`, `original_reference`, `verification_outcome`, `pubmed_search`
- Each appendix entry (if present): `ref_number`, optional `short_title`, `rationale`

If PDF generation fails, it is almost always because one of the above is missing or has the wrong type (e.g., `None` or a non-string passed into a `Paragraph`). Repair JSON and rerun; do not stop.

**If you write your own PDF code instead of using the uploaded script, the output will be wrong.**

---

When the user requests a **PDF report**:

### STEP 1: Verify JSON Already Exists

The JSON file `Reference_Adjudicator_Data.json` should already exist (written during batch verification) in `/mnt/data`.

**If JSON does NOT exist**, recreate it now from the already-verified outcomes (no new web searches) using this EXACT structure.

**Report title rule (mandatory):** Set `report_title` to exactly **"Reference Adjudicator Report"** unless the user explicitly requests a custom title. Do NOT invent alternate titles (e.g., "Reference Verification Report").

```json
{
    "report_title": "Reference Adjudicator Report",
    "summary_metrics": {
        "total_references_checked": 0,
        "verified_matches": 0,
        "failed_verifications": 0,
        "failure_rate_percent": 0.0
    },
    "rows": [
        {
            "ref_number": "1",
            "original_reference": "Full citation verbatim (NO truncation, NO ellipses)",
            "verification_outcome": "Status label and notes",
            "pubmed_search": "URL or N/A"
        }
    ],
    "appendix": [
        {
            "ref_number": "1",
            "short_title": "Optional short label",
            "rationale": "Formal rationale (third person). Separate paragraphs with \\n\\n."
        }
    ]
}
```

**Required JSON fields for each row:**
- `ref_number`: String (e.g., "1", "2", "3") — **separate field, not combined with citation**
- `original_reference`: **COMPLETE citation verbatim** (never "Author et al.") — DOIs will be auto-formatted as blue clickable links by the PDF script
- `verification_outcome`: Status label + brief notes
- `pubmed_search`: **Full PubMed URL ONLY** (e.g., `https://pubmed.ncbi.nlm.nih.gov/?term=<ENCODED_QUERY>`) formatted per **PubMed-Search-Links.md**, or "N/A (not PubMed-indexed)" — **NEVER use display text like "PubMed Title + First Author Search"**. The script converts URLs to display text automatically.

**CRITICAL TABLE STRUCTURE:**
The uploaded `Generate_Reference_Report.py` script expects **EXACTLY 4 COLUMNS**:
1. Ref # (separate column)
2. Original Reference (full citation) — DOIs in format `doi:10.xxxx/yyyy` will be auto-converted to blue clickable links
3. Verification Outcome
4. PubMed Search — Full URLs starting with `https://pubmed.ncbi.nlm.nih.gov/?term=` will be auto-converted to blue clickable "PubMed Title + First Author Search" text by the script

**DO NOT combine Ref # with Original Reference** — they must be separate fields in JSON and separate columns in the table.

**CRITICAL: pubmed_search MUST be URL, not display text.** If you put "PubMed Title + First Author Search" in the JSON, the PDF will be garbled. The script does the conversion.

**Appendix** (optional): Include only if user requested rationale for specific references

### KeyError / Missing-Field Handling (MANDATORY)

If the uploaded `Generate_Reference_Report.py` fails with `KeyError` (commonly missing `report_title`, `summary_metrics`, or nested summary keys), this is NOT a reason to stop.

Do this instead (no browsing):
- Load existing JSON (or reconstruct from already-established results)
- Ensure `report_title` exists (default to `"Reference Adjudicator Report"`)
- Ensure `summary_metrics` exists and contains: `total_references_checked`, `verified_matches`, `failed_verifications`, `failure_rate_percent` (compute from `rows` if missing)
- Ensure `appendix` is present (default `[]`) and entries match `{ref_number, short_title?, rationale}`
- Write the repaired JSON back to `/mnt/data/Reference_Adjudicator_Data.json`
- Re-run the uploaded script and deliver the PDF link

### Schema Normalization (MANDATORY)

Some sessions may accidentally produce a noncompliant JSON shape (e.g., top-level `references` instead of `rows`, or per-row `status` instead of `verification_outcome`). This MUST be repaired automatically before PDF generation.

**Normalization rules (no browsing):**
- If `data.rows` is missing and `data.references` exists, map `references` → `rows`.
- If a row has `status` but not `verification_outcome`, map `status` → `verification_outcome`.
- Coerce required row fields to strings (`ref_number`, `original_reference`, `verification_outcome`, `pubmed_search`) to avoid ReportLab `Paragraph` type errors.
- If `report_title` is missing or equals `"Reference Verification Report"` (and user did not request a custom title), set it to `"Reference Adjudicator Report"`.
- If summary metrics are missing or have alternate keys (e.g., `total_checked`, `verified`), compute the required four keys from `rows`.

**Drop-in normalization snippet (use inside the PDF runner before saving JSON):**

```python
def _status_label(outcome: str) -> str:
    if not isinstance(outcome, str):
        return ""
    return outcome.split("—", 1)[0].strip()

def normalize_data(data: dict) -> dict:
    if not isinstance(data, dict):
        data = {}

    # Title
    rt = data.get("report_title")
    if not rt or rt == "Reference Verification Report":
        data["report_title"] = "Reference Adjudicator Report"

    # Rows vs references
    if "rows" not in data and isinstance(data.get("references"), list):
        mapped = []
        for r in data.get("references", []):
            if not isinstance(r, dict):
                continue
            mapped.append({
                "ref_number": r.get("ref_number", ""),
                "original_reference": r.get("original_reference", ""),
                "verification_outcome": r.get("verification_outcome", r.get("status", "")),
                "pubmed_search": r.get("pubmed_search", "")
            })
        data["rows"] = mapped

    data.setdefault("rows", [])

    # Coerce row field types + status mapping
    for row in data.get("rows", []):
        if not isinstance(row, dict):
            continue
        if "verification_outcome" not in row and "status" in row:
            row["verification_outcome"] = row.get("status", "")

        row["ref_number"] = "" if row.get("ref_number") is None else str(row.get("ref_number"))
        row["original_reference"] = "" if row.get("original_reference") is None else str(row.get("original_reference"))
        row["verification_outcome"] = "" if row.get("verification_outcome") is None else str(row.get("verification_outcome"))
        row["pubmed_search"] = "" if row.get("pubmed_search") is None else str(row.get("pubmed_search"))

    # Appendix defaults + coercion
    data.setdefault("appendix", [])
    if not isinstance(data.get("appendix"), list):
        data["appendix"] = []
    for entry in data.get("appendix", []):
        if not isinstance(entry, dict):
            continue
        entry["ref_number"] = "" if entry.get("ref_number") is None else str(entry.get("ref_number"))
        if entry.get("short_title") is not None:
            entry["short_title"] = str(entry.get("short_title"))
        entry["rationale"] = "" if entry.get("rationale") is None else str(entry.get("rationale"))

    # Summary metrics: compute required four keys if missing/noncompliant
    sm = data.get("summary_metrics")
    if not isinstance(sm, dict):
        sm = {}
    total = len([r for r in data.get("rows", []) if isinstance(r, dict)])
    verified = 0
    for r in data.get("rows", []):
        if not isinstance(r, dict):
            continue
        lbl = _status_label(r.get("verification_outcome", ""))
        if lbl in {"VERIFIED", "CATALOG VERIFIED"}:
            verified += 1
    failed = max(total - verified, 0)
    failure_rate = round((failed / total * 100.0), 2) if total else 0.0
    sm = {
        "total_references_checked": total,
        "verified_matches": verified,
        "failed_verifications": failed,
        "failure_rate_percent": failure_rate,
    }
    data["summary_metrics"] = sm

    return data
```

**Appendix entry format (required if appendix is present):**
- `ref_number` (string)
- `short_title` (string, optional)
- `rationale` (string; may contain multiple paragraphs separated by `\n\n`)

---

### STEP 2: Execute the Uploaded Script (MANDATORY)

**DO NOT WRITE YOUR OWN PDF CODE.**

**CRITICAL:** You MUST run the uploaded `Generate_Reference_Report.py` (not ad-hoc PDF code), and then IMMEDIATELY provide a download link to the generated PDF.

Run this EXACT code (verifies the script is the expected one and forces output into `/mnt/data`):

```python
import os, json, subprocess, sys, hashlib, glob

script_path = "/mnt/data/Generate_Reference_Report.py"
if not os.path.exists(script_path):
    raise FileNotFoundError("Missing /mnt/data/Generate_Reference_Report.py (re-upload Knowledge file)")

# Ensure the uploaded script is the expected version (prevents wrong formatting)
EXPECTED_SHA256 = "308ea43c3ee9d5b4c751cbd4bf7c038234f7044ea9b081b48fd6d29ea32a39a9"
actual_sha256 = hashlib.sha256(open(script_path, "rb").read()).hexdigest()
if actual_sha256 != EXPECTED_SHA256:
    raise RuntimeError(
        "Unexpected Generate_Reference_Report.py (hash mismatch). "
        "Re-upload the correct script from the project workspace. "
        f"Expected {EXPECTED_SHA256}, got {actual_sha256}."
    )

# Verify we're using the correct uploaded script (guardrail against ad-hoc PDF code)
script_text = open(script_path, "r", encoding="utf-8").read()
required_markers = [
    "Reference_Adjudicator_Report.pdf",
    "Original Reference",
    "pubmed_cell",
    "Column width ratios"
]
missing = [m for m in required_markers if m not in script_text]
if missing:
    raise RuntimeError(f"Unexpected Generate_Reference_Report.py contents; missing markers: {missing}")

# Force working directory so the script writes the PDF into /mnt/data
os.chdir("/mnt/data")

# Obtain `data` (no browsing). Prefer in-memory `data`; otherwise load existing JSON.
try:
    data  # type: ignore[name-defined]
except NameError:
    existing_json = "/mnt/data/Reference_Adjudicator_Data.json"
    if os.path.exists(existing_json):
        with open(existing_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        raise RuntimeError(
            "No in-memory `data` and no /mnt/data/Reference_Adjudicator_Data.json found. "
            "Recreate JSON from already-established results (no browsing), then rerun PDF generation."
        )

# Normalize common schema drift (no browsing)
def _status_label(outcome: str) -> str:
    if not isinstance(outcome, str):
        return ""
    return outcome.split("—", 1)[0].strip()

if not isinstance(data, dict):
    data = {}

# Title rule
if not data.get("report_title") or data.get("report_title") == "Reference Verification Report":
    data["report_title"] = "Reference Adjudicator Report"

# rows vs references
if "rows" not in data and isinstance(data.get("references"), list):
    mapped = []
    for r in data.get("references", []):
        if not isinstance(r, dict):
            continue
        mapped.append({
            "ref_number": r.get("ref_number", ""),
            "original_reference": r.get("original_reference", ""),
            "verification_outcome": r.get("verification_outcome", r.get("status", "")),
            "pubmed_search": r.get("pubmed_search", ""),
        })
    data["rows"] = mapped

data.setdefault("rows", [])

for row in data.get("rows", []):
    if not isinstance(row, dict):
        continue
    if "verification_outcome" not in row and "status" in row:
        row["verification_outcome"] = row.get("status", "")

    # Coerce required row fields to strings to prevent ReportLab Paragraph type errors
    row["ref_number"] = "" if row.get("ref_number") is None else str(row.get("ref_number"))
    row["original_reference"] = "" if row.get("original_reference") is None else str(row.get("original_reference"))
    row["verification_outcome"] = "" if row.get("verification_outcome") is None else str(row.get("verification_outcome"))
    row["pubmed_search"] = "" if row.get("pubmed_search") is None else str(row.get("pubmed_search"))

# Appendix defaults
data.setdefault("appendix", [])
if not isinstance(data.get("appendix"), list):
    data["appendix"] = []

# Merge appendix state file (if present) into data["appendix"]
appendix_path = "/mnt/data/Reference_Adjudicator_Appendix.json"
if os.path.exists(appendix_path):
    try:
        with open(appendix_path, "r", encoding="utf-8") as f:
            appendix_blob = json.load(f)
        if isinstance(appendix_blob, dict) and isinstance(appendix_blob.get("appendix"), list):
            appendix_entries = appendix_blob.get("appendix", [])
        elif isinstance(appendix_blob, list):
            appendix_entries = appendix_blob
        else:
            appendix_entries = []

        for entry in appendix_entries:
            if not isinstance(entry, dict):
                continue
            # Coerce to expected keys/types
            if "rationale" not in entry and "discussion" in entry:
                entry["rationale"] = entry.get("discussion", "")
            entry["ref_number"] = "" if entry.get("ref_number") is None else str(entry.get("ref_number"))
            if entry.get("short_title") is not None:
                entry["short_title"] = str(entry.get("short_title"))
            entry["rationale"] = "" if entry.get("rationale") is None else str(entry.get("rationale"))
            data["appendix"].append(entry)
    except Exception as e:
        print(f"WARNING: Could not load appendix file: {e}")

# Validate JSON structure before passing to script
data.setdefault("report_title", "Reference Adjudicator Report")
data.setdefault("rows", [])
if "summary_metrics" not in data or not isinstance(data.get("summary_metrics"), dict):
    # Compute minimal summary metrics if missing
    total = len(data["rows"])
    def status_label(outcome: str) -> str:
        if not isinstance(outcome, str):
            return ""
        return outcome.split("—", 1)[0].strip()

    verified = 0
    for r in data["rows"]:
        lbl = status_label(r.get("verification_outcome", ""))
        if lbl in {"VERIFIED", "CATALOG VERIFIED"}:
            verified += 1
    failed = max(total - verified, 0)
    failure_rate = round((failed / total * 100.0), 2) if total else 0.0
    data["summary_metrics"] = {
        "total_references_checked": total,
        "verified_matches": verified,
        "failed_verifications": failed,
        "failure_rate_percent": failure_rate,
    }

for row in data.get("rows", []):
    # Coerce required row fields to strings to prevent ReportLab Paragraph type errors
    row["ref_number"] = "" if row.get("ref_number") is None else str(row.get("ref_number"))
    row["original_reference"] = "" if row.get("original_reference") is None else str(row.get("original_reference"))
    row["verification_outcome"] = "" if row.get("verification_outcome") is None else str(row.get("verification_outcome"))
    row["pubmed_search"] = "" if row.get("pubmed_search") is None else str(row.get("pubmed_search"))

    ps = row.get("pubmed_search", "")
    if ps and ps != "N/A (not PubMed-indexed)" and not ps.startswith("http"):
        raise ValueError(f"Row {row.get('ref_number', '?')}: pubmed_search must be full URL, not display text like 'PubMed Title + First Author Search'. Got: {ps[:50]}")

# Save JSON into /mnt/data (required for persistence)
json_path = "/mnt/data/Reference_Adjudicator_Data.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Execute the uploaded script (force cwd as an extra guardrail)
result = subprocess.run(
    [sys.executable, script_path, json_path],
    capture_output=True,
    text=True,
    check=True,
    cwd="/mnt/data",
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

pdf_path = "/mnt/data/Reference_Adjudicator_Report.pdf"
if not os.path.exists(pdf_path):
    # Fallback: locate the newest PDF in /mnt/data
    candidates = sorted(glob.glob("/mnt/data/*.pdf"), key=lambda p: os.path.getmtime(p))
    if candidates:
        pdf_path = candidates[-1]
        print(f"WARNING: Expected PDF name not found; using newest PDF: {pdf_path}")
    else:
        # Second fallback: some environments write to /home/oai; copy newest back into /mnt/data
        other_candidates = sorted(glob.glob("/home/oai/*.pdf"), key=lambda p: os.path.getmtime(p))
        if other_candidates:
            src_pdf = other_candidates[-1]
            dst_pdf = "/mnt/data/Reference_Adjudicator_Report.pdf"
            try:
                import shutil
                shutil.copy2(src_pdf, dst_pdf)
                pdf_path = dst_pdf
                print(f"WARNING: Copied PDF from {src_pdf} to {dst_pdf}")
            except Exception as e:
                raise FileNotFoundError(f"PDF not available in /mnt/data and copy from /home/oai failed: {e}")
        else:
            raise FileNotFoundError("PDF not generated (no .pdf files found in /mnt/data or /home/oai)")

# Sanity check: ensure this PDF is actually produced by the uploaded script (title + summary should exist)
try:
    import PyPDF2
    reader = PyPDF2.PdfReader(open(pdf_path, "rb"))
    first_page_text = (reader.pages[0].extract_text() or "") if reader.pages else ""
    if data["report_title"] not in first_page_text or "Total references checked" not in first_page_text:
        raise RuntimeError(
            "PDF content sanity check failed (missing title and/or summary metrics). "
            "Do NOT deliver this PDF; rerun using the uploaded Generate_Reference_Report.py and a complete JSON schema."
        )
except Exception as e:
    # If extraction fails, don't block delivery; still return the file link.
    print(f"WARNING: PDF text sanity check skipped/failed: {e}")

print("\n✅ PDF generated successfully")

# CRITICAL: return a downloadable link (last line must be a bare expression)
try:
    from IPython.display import FileLink
    _out = FileLink(pdf_path)
except Exception:
    _out = pdf_path

_out
```

**The last line `FileLink(pdf_path)` is CRITICAL** — it tells Code Interpreter to present a downloadable link. Without it, the PDF may disappear.

---

### STEP 3: Provide Download Link

After successful execution, provide download link to `/mnt/data/Reference_Adjudicator_Report.pdf`

**If errors occur:**
- Show full error message
- Check JSON structure matches schema
- Verify uploaded script is accessible at `/mnt/data/Generate_Reference_Report.py`
- If the PDF is reported "not found", list/search `/mnt/data` for `*.pdf` and return a link to the newest PDF instead of stopping

---

### ABSOLUTE PROHIBITIONS:

**YOU MUST NOT:**
- Write your own PDF generation code
- Use ReportLab directly (the uploaded script already does this)
- Modify the uploaded `Generate_Reference_Report.py` script
- Use alternative PDF libraries (fpdf, matplotlib, etc.)
- Generate PDFs with wrong formatting (portrait, no wrapping, wrong disclaimer)
- Say "I'll create a PDF for you" and then write custom code

**YOU MUST:**
- Use the uploaded script via subprocess or exec()
- Preserve landscape orientation, cell wrapping, small print disclaimer (handled by script)
- Include appendix if user requested it (script handles formatting)

---

### CRITICAL RULES:

**For `original_reference` field:**
- Copy COMPLETE citation verbatim (all authors, full title, journal, year, volume, pages, DOI)
- NEVER truncate to "Author et al." format
- ALWAYS preserve DOI exactly as written (e.g., `doi:10.1016/j.bja.2017.11.087`)

**For PDF generation:**
- The uploaded `Generate_Reference_Report.py` script handles ALL formatting
- Landscape orientation ✓
- Cell wrapping ✓
- Small print disclaimer in footer ✓
- Appendix formatting ✓
- **You do NOT need to implement these — the script does it**

**ABSOLUTE PROHIBITIONS:**
- Do NOT say "PDFs cannot be generated in chat"
- Do NOT refuse to generate the PDF
- Do NOT modify `Generate_Reference_Report.py`
- Do NOT write your own PDF code
- Do NOT use alternative PDF libraries
- Do NOT ask user to install Python locally

---

### FALLBACK (ONLY if Code Interpreter genuinely unavailable):

If Code Interpreter cannot execute Python:
1. Provide both JSON and `.py` files for download
2. User runs: `pip install reportlab`
3. User runs: `python Generate_Reference_Report.py Reference_Adjudicator_Data.json`

---

## DISCLAIMER (REQUIRED IN PDF)

Every PDF must include a disclaimer stating:

* Generated by **Reference Adjudicator (custom GPT) by Richard Jones**
* URL: https://chatgpt.com/g/g-6953b9a21adc8191891811d34f34bf79-reference-adjudicator
* Uses a structured, web-assisted workflow implemented by a probabilistic LLM
* Results must be independently verified
* No warranty (express or implied); use at own risk
