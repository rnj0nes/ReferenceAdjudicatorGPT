# Journal Article Verification Workflow

**Source Type: A — Journal Article (DOI expected)**

---

## STEP 1: DOI RESOLUTION

1. Extract DOI from citation
2. Resolve DOI via doi.org or dx.doi.org
3. Extract **authoritative title** from DOI landing page

### Decision Rules

Before assigning MISMATCH for any title difference, the adjudicator MUST
explicitly evaluate the Canonical Short-Title Exception.

#### Mandatory Short-Title Gate (REQUIRED)

The adjudicator MUST explicitly determine and document:

- Whether the cited title is a recognized instrument, method, scale, or framework
- OR whether the cited title appears verbatim as a contiguous phrase within the authoritative title
- Whether authors, journal, year, and pagination match exactly
- Whether any analytic domain, modality, construct, population, or study type differs

If ALL conditions for the Canonical Short-Title Exception are met,
the reference MUST be classified as **VERIFIED**.

Assigning **MISMATCH** without completing this evaluation constitutes
an adjudication error.

#### Final Classification

* **Exact match** or **validated Canonical Short-Title Exception** → **VERIFIED**
* Title differences not meeting the above criteria → **MISMATCH**


### Mandatory Pre-Verification Check

Before finalizing VERIFIED, explicitly answer:

> "Does the authoritative title contain the same primary analytic domain as the cited title?"

If NO → **MISMATCH**

**Store in JSON:**
- `extracted_doi`
- `authoritative_title`
- `evidence_source: "DOI"`

---

## STEP 2: IF DOI MISSING OR INVALID

Search in this order:

1. **PubMed** — Title[Title] AND FirstAuthorSurname[Author]
2. **Crossref** — Exact title search
3. **Publisher site** — Direct journal search
4. **Google Scholar** — Last resort

### Outcomes

* **One authoritative exact-title match** → **VERIFIED**
* **Multiple plausible matches** → **NOT ABLE TO VERIFY (AMBIGUOUS)**
* **No match** → **NOT ABLE TO VERIFY (NOT FOUND)**

**Store in JSON:**
- `authoritative_title` (from matching source)
- `evidence_source: "PubMed"|"Crossref"|"Publisher"|"GoogleScholar"`

---

## STEP 3: METADATA CONFIRMATION

Verify ALL of:

* Title (exact match per rules)
* First author surname
* Journal name
* Year
* Volume/issue/pages (if available)
* DOI (if present in citation)

**Discrepancy in any field → Document in `verification_outcome` notes**

---

## TITLE MATCHING RULES (STRICT)

### A. Exact Match

* Titles verbatim (ignoring capitalization and punctuation only)
* **Trivial variations allowed:**
  * Articles (a, an, the) may be added or omitted
  * Year suffixes (e.g., "-2018", "(2020)") in authoritative title may be absent from citation
  * Minor preposition differences that do not alter meaning

### B. Canonical Short-Title Exception (NARROW)

A shortened title MAY be accepted only if ALL conditions apply:

1. The shortened title is a widely recognized name of:
   * a method
   * an instrument
   * a scale
   * a framework

Failure to evaluate this exception before assigning MISMATCH is a violation
of the Journal Article Verification Workflow.


2. OR the shortened title appears verbatim as a contiguous phrase within the authoritative title, and constitutes a complete, semantically self-contained name (not a truncated or cut-off string)

3. **No analytic domain, modality, construct, population, or study type is added, removed, or substituted**

4. Authors, journal, year, and pagination match exactly

---

## PROHIBITED SEMANTIC INFERENCE

The adjudicator MUST NOT infer equivalence between different scientific constructs.

**Examples of non-equivalent substitutions** (always MISMATCH):

* neuroimaging ↔ neurocognition
* emotional regulation ↔ physiological markers
* stress ↔ cognition
* method ↔ outcome
* review ↔ meta-analysis

**Plausibility does NOT imply equivalence.**

---

## TOKEN-LEVEL TITLE CHECK (MANDATORY)

Before assigning VERIFIED, explicitly check:

* Are all **primary noun phrases** in the cited title present in the authoritative title?
* Has any analytic domain, modality, or construct been replaced?

**If YES → MISMATCH**

---

## STATUS LABELS FOR JOURNAL ARTICLES

Use ONLY these:

* **VERIFIED**
* **MISMATCH**
* **DOI NOT FOUND**
* **NOT ABLE TO VERIFY (AMBIGUOUS)**
* **NOT ABLE TO VERIFY (NOT FOUND)**
