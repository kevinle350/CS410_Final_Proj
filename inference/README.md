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