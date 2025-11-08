from pdf_summarization import generate_paper_summary
from paper_filtering import get_most_interesting_papers

def generate_article_report(article_filename: str)->None:
    """
    Generate a markdown report of the given article.
    The article should be in the directory configured (`papers_path`) in the ini file,
    and the report will be saved to the `reports_path` directory.
    :param article_filename: Filename (not full path) of the article.
    """
    generate_paper_summary(article_filename)

def get_interesting_papers(no_papers: int)->None:
    """
    Print information about most interesting papers from the domains configured in the ini file.
    :param no_papers: Number of most interesting papers to print information about.
    """
    for x in get_most_interesting_papers(no_papers):
        print(x)


if __name__ == '__main__':
    # Example usage
    get_interesting_papers(10)
    generate_article_report("2510.14837v1.pdf")