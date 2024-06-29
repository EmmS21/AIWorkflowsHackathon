import os
from crewai import Agent, Task, Crew
from arxivController import SearchArxiv
import arxiv

os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI')
client = arxiv.Client()
search_arxiv_instance = SearchArxiv

researcher = Agent(
    role='Researcher',
    goal='Generate topics in artificial intelligence and software engineering to help me learn',
    verbose=True,
    memory=True,
    backstory=(
        'The Researcher is an agent with a PhD in Computer Science, specializing in Artificial Intelligence and Software Engineering.'
        'Having worked as a senior researcher at a top-tier university, the Researcher has published numerous papers in prestigious journals'
        'and conferences. With a passion for advancing knowledge and helping others learn, the Researcher has developed sophisticated '
        'natural language processing techniques to analyze and synthesize research papers from arXiv. The agent is dedicated to curating '
        'cutting-edge topics that align with your learning goals, providing you with the most relevant and up-to-date information in '
        'Software Engineering and AI.'
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
    description="Select 1 topic in any of the fields, passing in the topics selected as a query into the search_tool",
    expected_output="A JSON containining; the field, and the topic selected for each field",
    agent=researcher,
)

get_articles = Task(
    description="Randomly select an article. If, based on the summary of the articles you find other related articles (ie. research papers directly related to the paper you chose), select these too. Do not select more than 3 papers",
    expected_output="Links to PDFs for each article selected",
    agent=search_and_select
)

my_crew = Crew(agents=[researcher, search_and_select, summarizer], tasks=[fetch, get_articles])
crew = my_crew.kickoff()

# Print the summaries
for article in crew['get_articles']['output']:
    print(f"Summary for article {article['pdf_links']}:\n{article['summary']}\n")