### ResearchDigest

* Retrieve information about new articles from arXiv 
* Automatically sort by article novelty and impact
* Generate markdown reports about a given paper containing its:
  * Summary
  * Simplified explanation of what it does
  * Potential applications, impact and disadvantages of the presented method
* Also includes a Langchain arXiv search tool for agentic usage (example usage in `arxiv_tool_agentic_usage.ipynb`)

---
#### Usage
The main user-facing functions, as well as usage examples can be found in the `research_digest.py` file.

Before running it, make sure to configure the necessary entries in `config.ini` - in particular, 
set up the API key for Google AI Studio, change the retrieved topics to ones you're interested in and disable Tesseract
if you don't have it installed.

For paper summarization, put the PDF in the `papers` directory and provide its filename as an argument 
to the function generating the reports.

---

PDF summarization can either use built-in pdfplumber text extraction or OCR.

The second option requires Tesseract to be installed and configured.  

The relevant `config.ini` entry should point to the tesseract executable.

---

Due to the large context window of Gemini 2.5 Flash, summarization uses the stuff method instead of map-reduce. 

This also helps with staying under the 250 requests per day limit of the free tier of Google AI Studio.

---

Thank you to arXiv for use of its open access interoperability.

*This project is not affiliated in any way with arXiv or Cornell University.*