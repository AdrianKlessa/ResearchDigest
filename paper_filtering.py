import statistics
from typing import Sequence

from arxiv_api_client import get_papers
from arxiv_api_tool import paper_to_str
from pydantic import BaseModel, Field
from model import get_llm
from parse_config import get_interests
import time

class PaperRating(BaseModel):
    """Rating of an ArXiv paper."""
    paper_id: str = Field(description="The arxiv id of the paper")
    title: str = Field(description="The title of the paper")
    novelty: int = Field(description="How novel the idea of the paper is (1-5)")
    clarity: int = Field(description="How understandable the presented idea is (1-5)")
    impact: int = Field(description="How impactful the paper might be (1-5)")
    comment: str = Field(description="Why the paper might be interesting (one sentence)")

class PaperRatings(BaseModel):
    paper_ratings: Sequence[PaperRating] = Field(..., description="Ratings of the papers")

def get_summary_paper_score(paper_rating: PaperRating):
    return statistics.mean([paper_rating.novelty, paper_rating.clarity, paper_rating.impact])

def get_paper_ratings():
    interests = get_interests()
    papers = []
    for interest in interests:
        papers.extend(get_papers(interest, 20, 0, True))
        time.sleep(3.5) # ArXiv API has a 1 request per 3 seconds rate limit
    papers = [paper_to_str(x) for x in papers]
    papers = "\n---\n".join(papers)
    llm = get_llm()
    structured_llm_json = llm.with_structured_output(PaperRatings, method="json_schema")

    # Gemini-2.5-flash has a 1M context window so splitting up the documents is likely not needed - they're just abstracts

    query = "Rate the novelty, clarity and impact of the following papers. Provide a comment on why the paper might be interesting."
    query = query + "\n\n\n" + papers
    result = structured_llm_json.invoke(
        query
    )
    return result

def sort_papers(paper_ratings: PaperRatings)->Sequence[PaperRating]:
    papers_by_score = [paper_rating for paper_rating in paper_ratings.paper_ratings]
    papers_by_score.sort(key=lambda p: get_summary_paper_score(p), reverse=True)
    return papers_by_score

def get_most_interesting_papers(n: int):
    ratings = get_paper_ratings()
    sorted = sort_papers(ratings)
    return sorted[:n]

if __name__ == "__main__":
    print(get_most_interesting_papers(5))