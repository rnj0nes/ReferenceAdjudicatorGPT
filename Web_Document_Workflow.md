# Web Document Verification Workflow

**Source Type: C — Web Document (reports, standards, guidelines; DOI not expected)**

---

## DEFINITION

Web documents include:

* Government reports
* Technical standards (ISO, IEEE, etc.)
* Clinical guidelines
* White papers
* Preprints (arXiv, bioRxiv, etc.)
* Institutional publications
* Data repositories

**Characteristics:**
* Published online with stable URL
* Issued by authoritative body
* May have version numbers or revision dates
* DOI optional but not expected

---

## STEP 1: IDENTIFY ISSUING BODY

Confirm the authoritative source:

* Government agency (CDC, NIH, WHO, etc.)
* Standards organization (ISO, NIST, IEEE, etc.)
* Professional society (APA, AMA, etc.)
* University/research institution
* Preprint server (arXiv, bioRxiv, medRxiv, etc.)

**If issuing body cannot be confirmed → NOT ABLE TO VERIFY**

---

## STEP 2: TITLE VERIFICATION

Search issuing body's website or repository for:

* **Exact title** (or close variant with minor wording differences)
* Document type (report, guideline, standard, etc.)
* Version/revision identifier

**Title matching rules:**
* More flexible than journal articles
* Minor wording differences acceptable if semantically equivalent
* Document number/ID must match if provided

---

## STEP 3: VERSION/DATE CONFIRMATION

Web documents often have multiple versions:

* **Cited version matches available version** → **VERIFIED (WEB DOCUMENT)**
* **Multiple versions exist, cited version unclear** → **NOT ABLE TO VERIFY (AMBIGUOUS)**
* **Cited version not found** → **NOT ABLE TO VERIFY (NOT FOUND)**

---

## STEP 4: URL STABILITY

Check if URL is:

* **Stable/persistent** (e.g., doi.org, handle.net, institutional repository)
* **Direct document link** (not homepage or search page)
* **Archived version** (Internet Archive acceptable if original unavailable)

**If URL is broken but document found elsewhere → Still VERIFIED if metadata matches**

---

## PREPRINTS (SPECIAL CASE)

Preprints may later be published in journals:

1. **Check if preprint exists** at cited repository (arXiv, bioRxiv, etc.)
2. **Verify preprint metadata** (title, authors, date, ID)
3. **Note if later published** in `verification_outcome` field, but status is based on preprint verification

**Example:**
```
VERIFIED (WEB DOCUMENT) — Preprint confirmed on bioRxiv (ID: 2023.01.15.524091). 
Note: Later published in Nature (2024) with modified title.
```

---

## DECISION RULES

| Scenario | Outcome |
|----------|---------|
| Exact title + issuing body confirmed + version matches | **VERIFIED (WEB DOCUMENT)** |
| Title close match + issuing body confirmed + version unclear | **NOT ABLE TO VERIFY (AMBIGUOUS)** |
| Issuing body confirmed but document not found | **NOT ABLE TO VERIFY (NOT FOUND)** |
| Cannot confirm issuing body | **NOT ABLE TO VERIFY (NOT FOUND)** |
| Multiple documents with similar titles from same body | **NOT ABLE TO VERIFY (AMBIGUOUS)** |

---

## WHAT TO STORE IN JSON

```json
{
  "ref_number": "15",
  "original_reference": "[Full citation verbatim]",
  "extracted_title": "Clinical Practice Guideline for the Management of Delirium",
  "extracted_first_author": "N/A",
  "authoritative_title": "Clinical practice guideline for the management of delirium in critically ill patients",
  "verification_outcome": "VERIFIED (WEB DOCUMENT) — Confirmed on Society of Critical Care Medicine website (version 2.1, 2023)",
  "pubmed_search": "N/A",
  "evidence_source": "SCCM.org"
}
```

---

## STATUS LABELS FOR WEB DOCUMENTS

Use ONLY these:

* **VERIFIED (WEB DOCUMENT)**
* **NOT ABLE TO VERIFY (AMBIGUOUS)**
* **NOT ABLE TO VERIFY (NOT FOUND)**

---

## COMMON SEARCH SOURCES

* **Issuing body website** — Primary source
* **Google Scholar** — Often indexes grey literature
* **Internet Archive (Wayback Machine)** — For dead links
* **Government repositories** — USA.gov, EUR-Lex, etc.
* **Preprint servers** — arXiv.org, bioRxiv.org, medRxiv.org, SSRN
* **Standards databases** — ISO.org, IEEE Xplore, NIST
