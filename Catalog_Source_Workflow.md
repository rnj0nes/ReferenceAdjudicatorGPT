# Catalog Source Verification Workflow

**Source Type: B — Catalog Source (books, manuals, instruments; DOI not expected)**

---

## WORK-LEVEL FIRST RULE (CRITICAL)

**Purpose:** Prevent false **CATALOG NOT FOUND** outcomes for books, manuals, and instruments with multiple editions or printings.

**Rule:** For catalog sources, verification must be **work-level first**, not edition-level.

---

## STEP 1: DETERMINE IF WORK EXISTS

Search WorldCat / Library of Congress / Publisher catalogs for:

* Title (exact or close variant)
* Author(s)
* Publisher (if provided)
* Work-level record (not specific edition)

**Question:** Does the work exist at all in authoritative catalogs?

---

## STEP 2: EDITION/YEAR MATCHING

**If work exists:**

### A. Citation specifies ISBN or explicit edition

* Search for that specific edition
* **Exact match found** → **CATALOG VERIFIED**
* **Edition not found but other editions exist** → **CATALOG FOUND – EDITION AMBIGUOUS**

### B. Citation does NOT specify ISBN or edition

* Work exists with multiple publication years/editions
* **Cited year is one of several known printings** → **CATALOG FOUND – EDITION AMBIGUOUS**
* **Work exists but cited year not in catalog** → **CATALOG FOUND – EDITION AMBIGUOUS**

### C. Single edition only

* Work has only one edition/printing in all catalogs
* **Metadata matches** → **CATALOG VERIFIED**

---

## PSYCHOMETRIC INSTRUMENTS & TEST MANUALS (SPECIAL RULE)

Instruments and test manuals from known publishers (e.g., WPS, Pearson, APA, Pro-Ed) are **presumed to have multiple printings** unless a specific edition or ISBN is provided.

**Examples:**
* Symbol Digit Modalities Test (SDMT)
* Wechsler Adult Intelligence Scale (WAIS)
* Beck Depression Inventory (BDI)

**Default outcome when year-only citation:**
* **CATALOG FOUND – EDITION AMBIGUOUS**

---

## DECISION ORDER (MANDATORY)

1. **Does the work exist at all?**
   * NO → **CATALOG NOT FOUND**
   * YES → proceed to step 2

2. **Can the cited edition/year be uniquely identified?**
   * YES (and matches) → **CATALOG VERIFIED**
   * NO (multiple editions, year ambiguous) → **CATALOG FOUND – EDITION AMBIGUOUS**

---

## GUARDRAIL

For known instruments, tests, or manuals with multiple historical printings:

**`CATALOG NOT FOUND` is disallowed** unless **no authoritative catalog record exists at all**.

---

## WHAT TO STORE IN JSON

```json
{
  "ref_number": "23",
  "original_reference": "[Full citation verbatim]",
  "extracted_title": "Symbol Digit Modalities Test (SDMT) Manual",
  "extracted_first_author": "Smith",
  "authoritative_title": "Symbol digit modalities test",
  "verification_outcome": "CATALOG FOUND – EDITION AMBIGUOUS — Work confirmed in WorldCat with multiple printings (1973, 1982, 1991); cited year (1982) is one of several documented editions",
  "pubmed_search": "N/A",
  "evidence_source": "WorldCat"
}
```

---

## STATUS LABELS FOR CATALOG SOURCES

Use ONLY these:

* **CATALOG VERIFIED**
* **CATALOG FOUND – EDITION AMBIGUOUS**
* **CATALOG NOT FOUND**

---

## COMMON SEARCH SOURCES

* **WorldCat** (OCLC) — Primary source for books/manuals
* **Library of Congress** — U.S. government publications, classic works
* **Publisher catalogs** — Direct lookup for instruments (WPS, Pearson, etc.)
* **Google Books** — Supplementary verification (use cautiously)
