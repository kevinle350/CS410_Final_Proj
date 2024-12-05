# Course Analyzer

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