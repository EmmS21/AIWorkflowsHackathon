import arxiv
from crewai_tools import tool
import os
import PyPDF2
import time

client = arxiv.Client()

class SearchArxiv:
    def __init__(self):
        self.client = arxiv.Client()

    @tool("Search Arxiv articles")
    def search_articles(query, max_results=2):
        """
        Searches for articles on arXiv based on a query.
        
        Args:
            query (str): The search query string.
            max_results (int): The maximum number of results to return (default is 100).

        Returns:
            list: A list of dictionaries containing article details (entry_id, title, pdf_url, summary).
        """ 
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        res = [
            {
                "entry_id": r.entry_id,
                "id": r.entry_id.split('/')[-1],
                "title": r.title,
                "pdf_url": r.pdf_url,
                "summary": r.summary
            }
            for r in client.results(search)
        ]
        return res
    
    @tool("Download research papers")
    def download_papers(article_id):
        """
        Searches and downloads article details from arXiv based on the article_id.

        Args:
            article_id (str): The ID of the article to fetch.

        Returns:
            pdf_path: A link to the extracted pdf
        """
        result = next(client.results(arxiv.Search(id_list=[article_id])))

        filename = f"{article_id}.pdf"            
        return result.download_pdf(filename=filename)

    # @tool("Extract text from pdf")
    # def extract_text(pdf_path):
    #     """
    #     Extracts the text from a downloaded pdf based on the path to the pdf.

    #     Args:
    #         pdf_path (str): A path to the downloaded PDF.

    #     Returns:
    #         text: Full article text
    #     """
    #     text = None
    #     with open(pdf_path, 'rb') as pdf_file:
    #         pdf_reader = PyPDF2.PdfReader(pdf_file)
    #         text = ''.join(page.extract_text() for page in pdf_reader.pages)
    #     return text


