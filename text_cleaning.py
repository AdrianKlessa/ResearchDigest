from typing import Sequence
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from model import get_llm

class CleanedParagraph(BaseModel):
    cleaned_text: str = Field(description="Paragraph cleaned of OCR and PDF text extraction artifacts.")

class CleanedDocument(BaseModel):
    cleaned_paragraphs: Sequence[CleanedParagraph] = Field(..., description="Sequence of paragraphs cleaned of OCR and PDF text extraction artifacts.")

cleanup_prompt_template = PromptTemplate.from_template("The following is the text of an"
                                                       " article which includes artifacts "
                                                       "caused by OCR and PDF text extraction."
                                                       "Return the same article as a sequence of cleaned paragraphs - "
                                                       "with added missing spaces between words and typos. "
                                                       "Remove any sections of text that are not intelligible English due to artifacts, "
                                                       "or that contain incorrectly parsed pseudocode or formulas."
                                                       "\n\n {article}")
def cleanup_article(article_text: str) -> str:
    """
    Clean the article text from OCR / PDF text extraction artifacts and return cleaned text.
    :param article_text: Text to clean
    :return: Cleaned text
    """
    llm = get_llm()
    prompt = cleanup_prompt_template.format(article=article_text)
    structured_llm_json = llm.with_structured_output(CleanedDocument, method="json_schema")
    result = structured_llm_json.invoke(
        prompt
    )
    cleaned_paragraphs = result.cleaned_paragraphs
    cleaned_text = ""
    for paragraph in cleaned_paragraphs:
        cleaned_text += paragraph.cleaned_text+"\n"
    return cleaned_text