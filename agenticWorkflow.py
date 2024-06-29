from flask import Flask, jsonify
import os
from crewai import Agent, Task, Crew
from arxivController import SearchArxiv
import arxiv

app = Flask(__name__)

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

summarize = Agent(
    role='Summarizer',
    goal='Produce a summarize explaining back a research paper with increasing levels of technical difficulty',
    verbose=True,
    memory=True,
    backstory=(
        'The Summarizer is an agent that is designed to help Software Engineers learn from researcg papers with increasing levels of complexity'
        'You will start off by explaining the article as though I am five, giving practical examples suited for your explanation'
        'With each proceeeding paragraph you will expand on your explanation, including examples in each step relevant to the level of expertise you are explaining'
        'You will include flash cards and MCQ type questions to test my understanding (include the answers to the questions at the end of the article)'
    )
)

teacher = Agent(
    role='Teacher',
    goal='Generate a study guide based on the summary of the summarizer',
    verbose=True,
    memory=True,
    backstory=(
        'The Teacher is an AI agent that specializes in the topic of the article'
        'Your role is to understand the summary of the article and create a study guide that will allow me to understand and learn what the summary of the article is about'
    )
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

introductory = Task(
    description="Explain the article back to me like I am 5 years old. Include, what the article is about, why this is important, the practical usage of this, how it can be used and what improvement this makes to existing methods",
    expected_output="Text summary",
    agent=summarize
)

my_crew = Crew(agents=[researcher, summarize], tasks=[fetch, get_articles, introductory])
# crew = my_crew.kickoff()

@app.route('/api/', methods=['GET'])
def kickoff():
    result = my_crew.kickoff()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
