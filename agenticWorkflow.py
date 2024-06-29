import os
from crewai import Agent, Task, Crew
from arxivController import SearchArxiv
import arxiv

os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI')
client = arxiv.Client()
search_arxiv_instance = SearchArxiv

researcher = Agent(
    role='Researcher',
    goal='Generate a random topic in artificial intelligence to help me learn',
    verbose=True,
    memory=True,
    backstory=(
        'The Researcher is an agent with a PhD in Computer Science, specializing in Artificial Intelligence.'
        'You role is to help Software Engineers learn more about Artificial Intelligence, picking topics most aligned with trends emerging in the space and useful for engineers venturing into AI'
    ),
    tools=[search_arxiv_instance.search_articles]
)

search_and_select = Agent(
    role='Select Articles',
    goal='Use a tool to search for articles in arxiv based on the provided topics and select a research paper',
    verbose=True,
    memory=True,
    backstory=(
        'The Select Articles is an agent with a PhD in Computer Science focused on teaching engineers based on research papers.' 
        'The agent reads all summaries, finds an article, looks through other summaries and either uses the summaries or the content from other articles to help engineers learn more about the chosen research paper'         
    ),
    tools=[search_arxiv_instance.download_papers]
)

summarizer = Agent(
    role='Summarizer',
    goal='Summarize the text of the research paper',
    verbose=True,
    memory=True,
    backstory=(
        'The Summarizer is an AI agent specialized in natural language processing and summarization. '
        'It uses advanced techniques to generate concise and informative summaries of research papers.'
    ),
    tools=[]
)

fetch = Task(
    description="Select 1 topic, passing in the topic selected as a query into the search_tool",
    expected_output="A JSON containining; the field, and the topic selected for each field",
    agent=researcher,
)

get_articles = Task(
    description="Randomly select an article. ",
    expected_output="Links to PDF for each article selected and a summary of this article",
    agent=researcher
)

my_crew = Crew(agents=[researcher, search_and_select, summarizer], tasks=[fetch, get_articles])
crew = my_crew.kickoff()

# Print the summaries
for article in crew['get_articles']['output']:
    print(f"Summary for article {article['pdf_links']}:\n{article['summary']}\n")