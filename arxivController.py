import arxiv
from crewai_tools import tool
import os

client = arxiv.Client()

class SearchArxiv:
    def __init__(self):
        self.client = arxiv.Client()

    @tool("Search Arxiv articles")
    def search_articles(query, max_results=100):
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
    
    # I think we might want to fetch the text from the PDF(s) provided
    # Extract text in chunks
    # use something like LlamaIndex to create an index and query the chunks
    # build a summary with each chunk 
    # continue to edit summary based on information extracted from each chunk
    # summary = 
    # i. explain in simple words, building in complexity (start off using every day examples, getting more technical and detailed with each paragraph)
    # ii. explain what the value of the paper is (why is this important - giving practical examples)
    # iii. Are there any formulas include, explain these to me simply (what do they mean in relation to the topic)
    # iv. What is the prior research that led to this development (what does this improve)
    # v. incluce a list of questions (progressively more technical) that I could answer to revise everything I learnt
    # vi. Is there anything I can build (simple project) to cement my understanding about things covered in this 

    # @tool("Download research papers")
    # def download_papers(article_id, download=True, filename=None, dirpath=None):
    #     """
    #     Fetches specific article details from arXiv based on the article_id.

    #     Args:
    #         article_id (str): The ID of the article to fetch.

    #     Returns:
    #         dict: A dictionary containing article details (entry_id, title, pdf_url, summary).
    #     """
    #     search = arxiv.Search(id_list=[article_id])
    #     results = list(client.results(search))

    #     if not results:
    #         return None
        
    #     article = results[0]
    #     pdf_path = None

    #     if download:
    #         if dirpath is None:
    #             dirpath = os.getcwd()
    #         if filename is None:
    #             pdf_path = article.download_pdf(dirpath=dirpath)
    #         else:
    #             pdf_path = article.download_pdf(dirpath=dirpath, filename=filename)

    #     return pdf_path
            

