from langchain.tools import tool
from arxiv_api_client import get_papers, Paper
import time

def paper_to_str(paper: Paper) -> str:
    return (
        f"id: {paper.id} \n"
        f"Title: {paper.title} \n"
        f"Authors: {paper.authors} \n"
        f"Published: {paper.published} \n"
        f"Summary {paper.summary} \n"
        f"PDF link: {paper.paper_pdf_link} \n"
    )


@tool
def get_arxiv_papers(query: str, max_results: int = 10, start: int = 0, last_month: bool = True)->str:
    """
    Retrieve paper information using arXiv API.
    :param query: String to search for
    :param max_results: Maximum number of papers to return. Shouldn't be too large to prevent overwhelming the API. Values above 500 are not supported.
    :param start: Start index for pagination (using 0-based indexing).
    :param last_month: Whether to only return papers published in the last month.
    :return: A string representation of the retrieved papers
    """
    print(f"Model called get_arxiv_papers with args: query={query}, max_results={max_results}, start={start}, last_month={last_month}")
    time.sleep(3.5) # No more than 1 request every 3 seconds
    if max_results > 500:
        max_results = 500
    papers = get_papers(query, max_results=max_results, start=start, last_month=last_month)
    papers_str = [paper_to_str(x) for x in papers]
    return "\n --- \n".join(papers_str)