import arxiv
from crewai_tools import tool

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
                "title": r.title,
                "pdf_url": r.pdf_url,
                "summary": r.summary
            }
            for r in client.results(search)
        ]
        return res
    
    def fetch_articles(self, article_id):
        search = arxiv.Search(
            id_list=[article_id]
        )
        results =  list(self.client.results(search))
        return results[0] if results else None
