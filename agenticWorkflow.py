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
    tools=[search_arxiv_instance.search_articles, search_arxiv_instance.download_papers]
)

blogger = Agent(
    role='Blog Poster',
    goal='Produce a detailed blog post explaining back a research paper with increasing levels of technical difficulty',
    verbose=True,
    memory=True,
    backstory=(
        'The Blogger is an agent that is designed to help Software Engineers learn from research papers with increasing levels of complexity'
        'You will produce a detailed blog explaining the selected research paper. This blog post should explain all concepts mentioned in the article with increasing levels of technical detail'
        'Include multiple paragraphs in the post based on the output from each of the tasks assigned to you'
    )
)

fetch = Task(
    description="Select 1 topic, passing in the topic selected as a query into the search_tool",
    expected_output="A JSON containining; the field, and the topic selected for each field",
    agent=researcher,
)

get_article = Task(
    description="Randomly select an article. ",
    expected_output="Links to PDF for the article selected",
    agent=researcher
)

read_full_article = Task(
    description="Download the pdf_url for the article and read the text output produced using the download_papers tool. Using the .txt file produced with the full research, produce a highly detailed blog post explaining back the article with incrementing detail. Each paragraph must explain every concept explored in the paper with increasing levels of complexity, starting off explaining everything to me like I am 5.",
    expected_output="Blog post explaining the article",
    agent=blogger
)

revision = Task( 
    description="Expand on the blog post by adding practical example for each concept explained. The examples should be incrementally more technical and detailed", 
    expected_output="Blog post with Practical Examples header for each practical example included.", 
    agent=blogger
)

add_flashcards = Task(
    description="Expand on the blog post by including flash cards and MCQ questions. For each concept explained, include flash cards and MCQs at the end of paragraphs with their own header. The questions should be aimed at testing my understanding of everything discussed in each paragraph. Include the answers to all the questions at the end of the article.",
    expected_output="Blog post with a header for the flashcards and MCQs included to clearly denote where they start",
    agent=blogger
)

additional_research = Task(
    description="Expand on the blog post by including links to other articles that could help build a more detailed understanding of everything covered in the research along with a link to the pdf_url of this research paper",
    expected_output="Add a paragraph to the blog post with the header Further Reading, this should include all research links with clear labels and a link to the pdf_url",
    agent=blogger
)

practical = Task(
    description="Expand on the blog post by giving 3-5 examples of simple practical Software Engineering projects I can build to put into practice what the research paper talks about. Include a detailed summary of each project idea, what the MVP would look like and how it would help me learn",
    expected_output="Add a paragraph to the blog post with the header Practical Examples, this should include all the practical examples",
    agent=blogger
)

compile_full = Task(
    description="Based on all the output from the previous texts, compile a full blog post with clear headers for each section",
    expected_output="Full text with headers as a markdown",
    agent=blogger
)


# my_crew = Crew(agents=[researcher, blogger], tasks=[fetch, read_full_article, revision, add_flashcards, additional_research, practical, compile_full ], output_log_file="output.md")
my_crew = Crew(agents=[researcher, blogger], tasks=[fetch, read_full_article, revision, add_flashcards, additional_research, practical, compile_full], output_log_file="output.txt")
crew = my_crew.kickoff()

# Read the content of the output.txt file
with open('output.txt', 'r') as file:
    lines = file.readlines()

# Initialize variables
filtered_lines = []
skip_lines = False

# Words to filter out
filtered_words = ["  File ", "raise_for_status", "For more information check", "INFO", "DEBUG", "Traceback", "During handling of the", "agent=", "status="]

# Iterate through each line
for line in lines:
    # Check if the line contains any of the filtered words
    if any(word in line for word in filtered_words):
        skip_lines = True
    elif skip_lines and line.strip() == "":
        skip_lines = False
    elif not skip_lines:
        filtered_lines.append(line)

# Write the filtered content back to the file
with open('output_cleaned.md', 'w') as file:
    # delete everything there before
    file.truncate(0)
    file.writelines(filtered_lines)