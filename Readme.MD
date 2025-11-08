### ResearchDigest

* Retrieve information about new articles from ArXiv 
* Automatically rate article novelty and impact
* Get AI-generated summaries for your convenience

PDF summarization can either use built-in pdfplumber text extraction or OCR.

The second option requires Tesseract to be installed and configured.  

The relevant `config.ini` entry should point to the tesseract executable.

---

Due to the large context window of Gemini 2.5 Flash, summarization uses the stuff method instead of map-reduce. 

This also helps with staying under the 250 requests per day limit of the free tier of Google AI Studio.

---

Thank you to arXiv for use of its open access interoperability.

*This project is not affiliated in any way with arXiv or Cornell University.*