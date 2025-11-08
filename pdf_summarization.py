from pathlib import Path

from text_cleaning import cleanup_article
from pdf_text_extraction import get_pdf_text
from model import get_llm
from langchain_core.prompts import PromptTemplate
from parse_config import get_reports_path, get_papers_path
import os

summarize_prompt = PromptTemplate.from_template("Summarize the following arXiv article to 500 words or less: \n\n {article}")
plain_english_prompt = PromptTemplate.from_template("Based on the following summary of an arXiv article, "
                                             "write a simplified explanation that could be understandable to "
                                             "an undergraduate student not acquainted well with this field: \n\n {article_summary}")
pros_cons_prompt = PromptTemplate.from_template("Based on the following summary of an arXiv article, "
                                                "write a list of positive and negative aspects of what was presented. "
                                                "Mention potential applications, impact, as well as drawbacks or aspects "
                                                "that might negatively influence wider application of what was presented (if applicable)."
                                                "Article: \n\n {article_summary}")

papers_path = get_papers_path()
reports_path = get_reports_path()

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

def assemble_report(article_id: str, article_summary: str, article_explanation: str, pros_cons: str)->str:
    markdown_report = ""
    markdown_report += f"# **Report for article {article_id}**"
    markdown_report += "\n\n# Technical summary \n\n"
    markdown_report += article_summary
    markdown_report += "\n\n# Simplified explanation \n\n"
    markdown_report += article_explanation
    markdown_report += "\n\n# Pros / cons \n\n"
    markdown_report += pros_cons
    return markdown_report

def save_report(report_markdown: str, filename: str)->None:
    file_path_pdf = os.path.join(reports_path, filename)
    file_path_markdown = Path(file_path_pdf).with_suffix(".md")
    with open(file_path_markdown, "w", encoding="utf-8", errors="ignore") as f:
        f.write(report_markdown)


def generate_paper_summary(article_filename: str)->None:
    article_path = os.path.join(papers_path, article_filename)

    extracted_text = get_pdf_text(article_path)
    cleaned_text = cleanup_article(extracted_text)
    article_summary = summarize_article(cleaned_text)
    article_explanation = explain_summary(article_summary)
    pros_cons = explain_summary_pros_cons(article_summary)

    assembled_report = assemble_report(article_filename, article_summary, article_explanation, pros_cons)
    save_report(assembled_report, article_filename)

if __name__ == "__main__":
    generate_paper_summary("2510.14837v1.pdf")