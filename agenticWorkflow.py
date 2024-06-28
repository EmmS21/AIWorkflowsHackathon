import os
from crewai import Agent, Task, Crew
from arxivController import SearchArxiv
import arxiv

os.environ['OPENAI_API_KEY'] = os.environ["OPEN_AI"]
client = arxiv.Client()
search_arxiv_instance = SearchArxiv

researcher = Agent(
    role='Researcher',
    goal='Generate topics in artificial intelligence and software engineering to help me learn',
    verbose=True,
    memory=True,
    backstory=(
        'The Researcher is an agent with a PhD in Computer Science, specializing in Artificial Intelligence and Software Engineering. '
        'Having worked as a senior researcher at a top-tier university, the Researcher has published numerous papers in prestigious journals '
        'and conferences. With a passion for advancing knowledge and helping others learn, the Researcher has developed sophisticated '
        'natural language processing techniques to analyze and synthesize research papers from arXiv. The agent is dedicated to curating '
        'cutting-edge topics that align with your learning goals, providing you with the most relevant and up-to-date information in '
        'Software Engineering and AI.'
    ),
    tools=[search_arxiv_instance.search_articles]
)

fetch = Task(
    description="Select 1 topic in each of the fields, passing in the topics selected as a query into the search_tool",
    expected_output="A JSON containining; the field, and the topic selected for each field",
    agent=researcher,
)


my_crew = Crew(agents=[researcher], tasks=[fetch])
crew = my_crew.kickoff()


# search_and_select = Agent(
#     role='Select Articles',
#     goal='Use a tool to search for articles in arxiv based on the provided topics and select 1-3 similar research papers',
#     verbose=True,
#     memory=True,
#     backstory=(
#         'The Select Articles, selects 1 or multiple research papers dealing with the topics selected by the Researcher. The Select Articles agent, ensures to select articles that can be read together to form a deeper understanding of the topic discussed. The Select articles agent will select only one article if the article needs to be read in isolation.'
#     )
# )