# Reference Adjudicator

A Custom GPT for independent, evidence-based verification of academic citations using live web searches.

You can use it now at Reference Adjudicator Custom GPT: [https://chatgpt.com/g/g-6953b9a21adc8191891811d34f34bf79-reference-adjudicator](https://chatgpt.com/g/g-6953b9a21adc8191891811d34f34bf79-reference-adjudicator)

## Overview

**Reference Adjudicator** is a ChatGPT Custom GPT designed to verify bibliographic references against authoritative online sources. It performs live lookups via DOI resolution, PubMed, Crossref, WorldCat, and other databases to confirm that citations are accurate and complete.

In the last few years, and especially since the widespread adoption of generative LLMs in scientific writing, “hallucinated references” have become a practical integrity problem: citations that look plausible but do not correspond to a real publication, or include a DOI that fails to resolve or resolves to a different work. Importantly, DOI/reference failures predate LLMs (copy‑paste propagation, metadata and XML tagging issues, and reference-manager export/linking bugs), so even non-AI manuscripts can contain broken or mismatched identifiers; what is newer is the scale and convincing realism of fabricated citations, making systematic verification increasingly valuable.

This tool is particularly useful for:
- Researchers validating reference lists before manuscript submission
- Journal editors or peer reviewers checking citation accuracy
- Librarians performing reference verification
- Academic integrity officers auditing publications
- Educators teaching citation verification practices
- Students learning proper referencing techniques
- Journalists fact-checking sources
- Anyone who needs systematic, documented citation checking

### Key Features

- **Live verification** — Uses real-time web searches, not cached or assumed data
- **Structured workflow** — Follows a strict, non-inferential verification process
- **Batch processing** — Handles large reference sets (20–50+) in manageable batches
- **PDF reports** — Generates PDF reports with clickable DOI and PubMed links
- **Appendix support** — Optionally includes detailed rationale for complex verification decisions
- **Cumulative tracking** — Maintains session state across multiple batches for complete final reports

---

## How to Use

### Setup (for GPT Creator)

1. Create a new Custom GPT in ChatGPT
2. Paste the contents of `Reference_Adjudicator_Instructions.md` into the **Instructions** field
3. Upload these files to **Knowledge**:
   - `Reference_Adjudicator_Knowledge.md`
   - `Generate_Reference_Report.py`
   - `PubMed-Search-Links.md`
4. Enable **Web Browsing** and **Code Interpreter** capabilities

### Basic Usage

1. **Upload your references** — Provide a document, spreadsheet, or text file containing numbered citations

2. **Request batch verification** — For large sets, verify in batches of ~12 to avoid timeouts:
   ```
   I've uploaded a document with 23 references for verification. 
   Please review them in batches of 12, maintaining a cumulative record 
   for the final PDF report. Let's start with references 1–12.
   ```

3. **Continue with subsequent batches**:
   ```
   Now verify 13–23.
   ```

4. **Generate the final report**:
   ```
   Generate the PDF report.
   ```

### Requesting Detailed Rationale (Optional)

If you want more detail on a specific verification decision:

```
Can you explain your reasoning for reference 14?
```

After discussion, you can add it to the report appendix:

```
Please add this explanation to the appendix.
```

---

## Example Outputs

### On-Screen Table

After each batch, Reference Adjudicator displays a table with:

| Ref # | Original Reference | Verification Outcome | PubMed Search |
|-------|-------------------|---------------------|---------------|
| 1 | Evered L, et al. Recommendations for nomenclature... doi:10.1016/j.bja.2017.11.087 | **VERIFIED** — Title, authors, journal, year, DOI all confirmed | [PubMed Search](https://pubmed.ncbi.nlm.nih.gov/?term=...) |
| 13 | Smith A. Symbol Digit Modalities Test (SDMT) Manual. 1982. | **CATALOG VERIFIED** — Found in WorldCat | N/A |

### Summary Metrics

```
Total references checked: 23
Verified matches: 21
Failed verifications: 2
Failure rate: 8.7%
```

### PDF Report

The generated PDF includes:
- Report title and timestamp
- Summary metrics
- Full verification table with clickable DOI and PubMed links
- Optional appendix with detailed rationale
- Disclaimer and attribution

---

## Status Labels

Reference Adjudicator uses these standardized status labels:

| Label | Meaning |
|-------|---------|
| **VERIFIED** | Citation confirmed via DOI or authoritative source |
| **MISMATCH** | DOI resolves to a different work than cited |
| **DOI NOT FOUND** | Provided DOI does not resolve |
| **NOT ABLE TO VERIFY (AMBIGUOUS)** | Multiple possible matches found |
| **NOT ABLE TO VERIFY (NOT FOUND)** | No matching record found |
| **CATALOG VERIFIED** | Book/manual found in WorldCat or publisher catalog |
| **CATALOG FOUND – EDITION AMBIGUOUS** | Multiple editions exist; specific edition unclear |
| **CATALOG NOT FOUND** | No catalog record found |
| **VERIFIED (WEB DOCUMENT)** | Web-based document confirmed at stable URL |

---

## File Inventory

| File | Purpose |
|------|---------|
| `Reference_Adjudicator_Instructions.md` | **Main instructions** — Paste into the Custom GPT's Instructions field. Contains core rules, verification workflows, and status labels. (~4,100 characters, under the 8,000 limit) |
| `Reference_Adjudicator_Knowledge.md` | **Extended knowledge base** — Upload to Knowledge. Contains detailed batch session workflow, appendix generation workflow, and complete PDF generation instructions with code templates. |
| `Generate_Reference_Report.py` | **PDF generator script** — Upload to Knowledge. Python script using ReportLab that the GPT executes via Code Interpreter to create professional PDF reports with clickable links and optional appendix. |
| `PubMed-Search-Links.md` | **PubMed query rules** — Upload to Knowledge. Specifies correct PubMed search syntax for Title + Author queries and URL encoding rules. |
| `Test_Citations.txt` | **Example input** — Sample set of 23 academic references for testing the system. |
| `Reference_Adjudicator_Report.pdf` | **Example output** — Sample PDF report generated from Test_Citations.txt. |

---

## Technical Notes

### Why Batch Processing?

Large reference sets (20+ citations) can cause:
- GPT timeouts during extended web searches
- Incomplete verification if the model rushes through too many at once
- Context window limitations

Batches of ~12 references balance thoroughness with reliability.

### Cumulative Session Tracking

The GPT maintains a "master record" of all verified references across batches within a single conversation. This ensures the final PDF includes everything, not just the last batch processed.

### PDF Generation

PDFs are generated using Python's ReportLab library via Code Interpreter. The GPT:
1. Writes verification data to a JSON file
2. Executes the uploaded `Generate_Reference_Report.py` script
3. Provides a download link to the generated PDF

### Why and how I made this

Just pasting in references into a ChatGPT (or Gemini) chat will not return the desired results. For the same reason that LLMs generate hallucinated references, LLMs in chat mode will identify provided references as "real" regardless of whether or not they match entries in reputable data sets. This Agentic AI tool was developed with ChatGPT and Claude Opus 4.5 running inside MS Visual Studio. The experience was fun and seamless. Although the Custom GPT don't seem to have a "syntax" the way I am used to (I am a data analyst and my day job is in R, Stata, etc.), there is a way of asking for ChatGPT to do things, and Claude was a lot of help with that.

I have tested these instructions in Gemini and the results are not satisfactory. The results in ChatGPT are not 100% reliable. In the tester reference set, there is one reference (Thayer et al, 2012) that sometimes is counted as a verified and sometimes not verified. This reference in the tester set as a title that is not exactly what matches the DOI Crossref entry. Whether or not it's a match and a typo versus something else is why this tool and all other AI tools require human supervision and double checking.

---

## Limitations

- **Requires live browsing** — Cannot verify references if web access is unavailable
- **Session-based** — Cumulative tracking is lost if you start a new conversation
- **DOI-dependent for journals** — Journal articles without DOIs require more extensive searching
- **No paywalled content** — Cannot verify content behind institutional paywalls

---

## License

This work is licensed under [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/).

You may share this material with attribution, but you may not use it commercially or distribute modified versions. See [LICENSE.md](LICENSE.md) for details.

---

## Author

**Richard Jones**

Reference Adjudicator Custom GPT: [https://chatgpt.com/g/g-6953b9a21adc8191891811d34f34bf79-reference-adjudicator](https://chatgpt.com/g/g-6953b9a21adc8191891811d34f34bf79-reference-adjudicator)
