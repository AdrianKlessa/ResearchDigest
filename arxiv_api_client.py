from dataclasses import dataclass
from datetime import datetime
import xml.etree.ElementTree as ET
import requests


API_URL = 'http://export.arxiv.org/api/query'
NAMESPACE = "{http://www.w3.org/2005/Atom}"

@dataclass
class Paper:
    id: str
    updated: datetime
    published: datetime
    title: str
    summary: str
    authors: list[str]
    paper_link: str
    paper_pdf_link: str

def clean_string(string: str) -> str:
    """
    Remove newlines and double spaces from the string
    :param string: String to clean
    :return: Cleaned string
    """
    return string.replace("\n", "").replace("  ", " ")

def get_papers(search_query: str, max_results: int = 20, start: int = 0) -> str:
    """
    Retrieve papers from arXiv API
    :param search_query: Text to search for
    :param max_results: Maximum number of papers to return
    :param start: Index of first paper to return (for batching results)
    :return: Pure-text response from arXiv API
    """
    params = {
        'search_query': search_query,
        'max_results': max_results,
        'start': start,
    }

    response = requests.get(API_URL, params=params)
    return response.text

def parse_atom_response(response: str)-> list[Paper]:
    """
    Parse XML response from arXiv API
    :param response: String response from arXiv API in the Atom XML format
    :return: List of Paper objects
    """
    root = ET.fromstring(response)
    papers = []
    for child in root:
        if child.tag == f'{NAMESPACE}entry':
            paper_id = None
            updated = None
            published = None
            title = None
            summary = None
            authors = []
            paper_link = None
            paper_pdf_link = None

            for element in child:
                if element.tag == f"{NAMESPACE}author":
                    authors.append(element.text)
                if element.tag == f"{NAMESPACE}id":
                    paper_id = element.text
                if element.tag == f"{NAMESPACE}updated":
                    updated = datetime.fromisoformat(element.text)
                if element.tag == f"{NAMESPACE}published":
                    published = datetime.fromisoformat(element.text)
                if element.tag == f"{NAMESPACE}title":
                    title = clean_string(element.text)
                if element.tag == f"{NAMESPACE}summary":
                    summary = clean_string(element.text)
                if element.tag == f"{NAMESPACE}link":
                    target = element.attrib['href']
                    if "pdf" in target:
                        paper_pdf_link = target
                    else:
                        paper_link = target

            paper = Paper(
                id=paper_id,
                updated=updated,
                published=published,
                title=title,
                summary=summary,
                authors=authors,
                paper_link=paper_link,
                paper_pdf_link=paper_pdf_link,
            )
            papers.append(paper)

    return papers
