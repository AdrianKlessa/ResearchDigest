from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import xml.etree.ElementTree as ET
import requests
from urllib.parse import quote


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

def datetime_to_arxiv_str(datetime_obj: datetime) -> str:
    """
    Converts a datetime object to a string in the format expected by the ArXiv API
    :param datetime_obj: Datetime object to convert
    :return: Datetime in the Arxiv API format
    """
    return datetime_obj.strftime("%Y%m%d%H%M")

def get_papers(search_query: str, max_results: int = 20, start: int = 0, last_month: bool = True) -> list[Paper]:
    """
    Retrieve papers from arXiv API
    :param search_query: Text to search for
    :param max_results: Maximum number of papers to return
    :param start: Index of first paper to return (for batching results)
    :param last_month: If true, return only papers published during the last month
    :return: List of Paper objects
    """

    params = {
        'max_results': max_results,
        'start': start,
    }
    if last_month:
        to_time = datetime.now(timezone.utc)
        from_time = to_time - timedelta(days=30)
        from_string = datetime_to_arxiv_str(from_time)
        to_string = datetime_to_arxiv_str(to_time)
        time_filter = f"submittedDate:[{from_string}+TO+{to_string}]"
        full_query = f"{search_query}+AND+{time_filter}"
        encoded_query = quote(full_query, safe=':+[]')
        params["search_query"] = encoded_query
    else:
        params["search_query"] = quote(search_query, safe=':+[]')

    url = f"{API_URL}?search_query={params['search_query']}&start={params['start']}&max_results={params['max_results']}"
    response = requests.get(url)
    return parse_atom_response(response.text)

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
                    authors.append(element.find(f"{NAMESPACE}name").text)
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

if __name__ == '__main__':
    #papers = get_papers("forecasting", last_month=True)

    with open("example_response.txt", "r") as f:
        raw_response = f.read()
        papers = parse_atom_response(raw_response)

    for paper in papers:
        print(paper.authors)
        print(f"Published: {paper.published}")

    print("---")
    print(str(papers[0]))