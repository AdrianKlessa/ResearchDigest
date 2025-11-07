from text_cleaning import cleanup_article
from pdf_text_extraction import get_pdf_text
from model import get_llm
from langchain_core.prompts import PromptTemplate

summarize_prompt = PromptTemplate.from_template("Summarize the following arXiv article to 500 words or less: \n\n {article}")
plain_english_prompt = PromptTemplate.from_template("Based on the following summary of an arXiv article, "
                                             "write a simplified explanation that could be understandable to "
                                             "an undergraduate student not acquainted well with this field: \n\n {article_summary}")
pros_cons_prompt = PromptTemplate.from_template("Based on the following summary of an arXiv article, "
                                                "write a list of positive and negative aspects of what was presented. "
                                                "Mention potential applications, impact, as well as drawbacks or aspects "
                                                "that might negatively influence wider application of what was presented (if applicable)."
                                                "Article: \n\n {article_summary}")

def summarize_article(article_text: str)->str:
    llm = get_llm()
    prompt = summarize_prompt.format(article=article_text)
    result = llm.invoke(prompt)
    result_text = result.content
    return result_text

def explain_summary(article_summary: str)->str:
    llm = get_llm()
    prompt = plain_english_prompt.format(article_summary=article_summary)
    result = llm.invoke(prompt)
    result_text = result.content
    return result_text

def explain_summary_pros_cons(article_summary: str)->str:
    llm = get_llm()
    prompt = pros_cons_prompt.format(article_summary=article_summary)
    result = llm.invoke(prompt)
    result_text = result.content
    return result_text

def print_pdf_report(pdf_path: str)->None:
    extracted_text = get_pdf_text(pdf_path)
    cleaned_text = cleanup_article(extracted_text)
    article_summary = summarize_article(cleaned_text)
    paper_explanation = explain_summary(article_summary)
    pros_cons = explain_summary_pros_cons(article_summary)
    print("------Final summary------")
    print("Summary of the arXiv article:")
    print(article_summary)
    print("Simplified explanation:")
    print(paper_explanation)
    print("Potential pros and cons of the presented method:")
    print(pros_cons)