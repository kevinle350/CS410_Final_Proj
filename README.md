# Course Analyzer

## Project Description
A problem that we find as students is finding the right courses to take for the upcoming semesters. There is so much information around and it is difficult to tailor information to a single place that can give a student a direct suggestion on whether or not a course should be taken or not and comparisons to other similar courses. We want to build a chatbot that will help students determine what classes to take based on their interests and course feedback. We plan to crawl data from https://uiucmcs.org/ and to take the students' comments into consideration when generating a response from the chatbot. Since this dataset is extremely small, we plan to compare the output of the chat-bot against the ranking of the implicit feedback, pseudo-relevant feedback, and relevant feedback output that we are able to find.

## Implementation Overview

The Course Analyzer project is implemented using a combination of Python and modern frameworks for web development and natural language processing. Here's a breakdown of the key components:

1. **Course Data Parsing**:
   - A JSONL file (`courses.jsonl`) contains structured course information, including titles, names, and detailed descriptions. The `course_parser` script allows for parsing and updating this dataset. This was achieved by the webcrawling.

2. **Natural Language Processing (NLP)**:
   - The `inference.py` script uses a pre-trained transformer model (`deepset/roberta-base-squad2`) to answer specific questions about courses. It processes each course's context and generates tailored responses to queries.

3. **Web Interface**:
   - The `webpage.py` script sets up a chatbot interface using Dash and Flask. Users can select courses and ask questions, receiving answers with confidence scores via auser-friendly web interface.

4. **Backend API**:
   - A Flask-based API allows querying the course data. This ensures efficient reuse of NLP models and easy integration with the chatbot front-end.

5. **Integration**:
   - The NLP model and web interface are seamlessly connected. When a user submits a query, the chatbot sends the input to the API, which processes the query and returns a result displayed in the chat.

Our implementation was verified based on expected output by manually looking at the data on the webpage and seeing the matchup based on the confidence score.


## Video Demo
Our team's video demo can be found [here](https://mediaspace.illinois.edu/media/t/1_noc04h09).

## TextData Proposal
Our team's project proposal can be found [here](https://textdata.org/submissions/671b1be2c2928a238422fd77).


## Initialize Repo
After you have cloned the repo, run the following command to install the necessary dependencies

    pip install -r requirements.txt

## Running Chatbot Webpage Locally
In a terminal, run the following to start the server:

    cd inference
    python inference.py

Then, in a new terminal window run the following to start the chatbot:

    python main.py

Open your web browser to http://127.0.0.1:8050/

# Course Parser
The parsed data results has already been added to the directory /course_parser/documents/courses.jsonl

The data is stored in the structure below 
```
{
        "course_title": title,
        "course_name": subtitle,
        "details": paragraphs
}
```
if you wish to run the parser locally or change the output structure

## Running Parser 

```
pip install -r requirements.txt

python3 course_parser.py
```

# Course Inference
The inference is based on Transformers with a pre-trained model to process and query course data

Currently the code is answering the question of "What is the focus of the course?"

we can connect this to the chatbot questions.

## Running Inference 

```
pip install -r requirements.txt

python3 inference.py
```


## Output Sample 

```
{"course_title": "Advanced Distributed Systems", "course_name": "CS 525", "answer": "Read lots (and lots and lots) of academic research papers on distributed computing", "score": 0.13518720865249634}
{"course_title": "Applied Machine Learning", "course_name": "CS 441", "answer": "Data science", "score": 0.5332742929458618}
{"course_title": "Cloud Computing Applications", "course_name": "CS 498", "answer": "understanding the architectural underpinnings", "score": 0.47364866733551025}

```