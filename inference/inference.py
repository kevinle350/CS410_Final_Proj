import json
from transformers import pipeline

def load_jsonl(file_path):
    """
    Load a JSONLines file containing multiple JSON objects.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]

def combine_course_details(course):
    """
    Combine fields of a single course object into a single context string.
    """
    context = f"Course Title: {course['course_title']}\n"
    context += f"Course Name: {course['course_name']}\n"
    context += "\n".join(course["details"])
    return context

def query_course(qa_pipeline, query, course):
    """
    Query the context of a single course and return the result.
    """
    context = combine_course_details(course)
    try:
        result = qa_pipeline(question=query, context=context)
        return {
            "course_title": course["course_title"],
            "course_name": course["course_name"],
            "answer": result['answer'],
            "score": result['score']
        }
    except Exception as e:
        print(f"Error querying course {course['course_title']}: {e}")
        return {
            "course_title": course["course_title"],
            "course_name": course["course_name"],
            "answer": None,
            "score": None
        }

def save_answers_to_jsonl(answers, output_path):
    """
    Save the answers into a JSONLines file.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        for answer in answers:
            file.write(json.dumps(answer) + '\n')

def main():
    # Path to JSONLines file
    jsonl_file = '../course_parser/documents/courses.jsonl'
    output_file = "single_answers.jsonl"

    # Load courses
    courses = load_jsonl(jsonl_file)

    # Load the QA pipeline
    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

    # Query to ask
    query = "What is the focus of the course?"


    # Process each course and save results
    answers = []
    for course in courses:
        print(f"Processing Course: {course['course_title']} ({course['course_name']})")
        result = query_course(qa_pipeline, query, course)
        answers.append(result)

    # Save the single answers
    save_answers_to_jsonl(answers, output_file)
    print(f"Single answers saved to {output_file}")


if __name__ == "__main__":
    main()