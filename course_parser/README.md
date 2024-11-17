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