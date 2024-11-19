import json
from transformers import pipeline
from flask import Flask, request, jsonify

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


# Additions for Backend API Integration
app = Flask(__name__)

# Load the courses and pipeline once for reuse
jsonl_file = '../course_parser/documents/courses.jsonl'
courses = load_jsonl(jsonl_file)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

@app.route('/query', methods=['POST'])
def query_api():
    """
    API endpoint for querying course information.
    Input: {"question": "<query>", "course_title": "<title>"}
    """
    data = request.json
    question = data.get("question")
    course_title = data.get("course_title")

    if not question or not course_title:
        return jsonify({"error": "Both 'question' and 'course_title' are required."})

    course = next((c for c in courses if c["course_title"].lower() == course_title.lower()), None)
    if not course:
        return jsonify({"error": f"Course with title '{course_title}' not found."})

    result = query_course(qa_pipeline, question, course)
    return jsonify(result)

if __name__ == "__main__":
    # main()  # Use this to run the existing script logic
    app.run(debug=True, host='0.0.0.0', port=5000)  # Use this to run the backend API