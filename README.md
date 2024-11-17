# Course Recommender

## Initialize Repo
After you have cloned the repo, run the following command to install the necessary dependencies

    pip install -r requirements.txt

## Running Chatbot Webpage Locally
In a terminal, run

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
cd course_parser

pip install -r requirements.txt

python3 course_parser.py
```
