import os
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import audio_handle

# load environment variables
_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

model = "gpt-4o"
temperature = 0.3
max_tokens = 500


def load_questions_from_json(json_file):
    with open(json_file, "r") as f:
        questions = json.load(f)
    return questions


def present_question(question_data):
    print(
        f"\n{question_data['question']['questionNumber']}- Question: {question_data['question']['question']}"
    )
    print("Choose one of the following options:")
    for key, value in question_data["answers"].items():
        print(f"{key}: {value}")


def evaluate_answers(questions):
    total_correct = 0
    total_difficulty = 0.0
    clo_incorrect_count = {}

    for question_data in questions:
        present_question(question_data)
        user_answer = input("Your answer (A, B, C, or D): ").strip().upper()

        correct_answer = question_data["correct_answer"]
        if user_answer == correct_answer:
            print("Correct!")
            total_correct += 1
            total_difficulty += int(question_data["difficulty"])
        else:
            print(f"Wrong. Correct answer was {correct_answer}.")
            clo = question_data["clo"]
            if clo in clo_incorrect_count:
                clo_incorrect_count[clo] += 1
            else:
                clo_incorrect_count[clo] = 1

    # Calculate user level
    if total_correct > 0:
        user_level = total_difficulty / total_correct
    else:
        user_level = 0.0

    # Determine CLO with the most incorrect answers
    most_incorrect_clo = max(clo_incorrect_count, key=clo_incorrect_count.get)

    # Print results
    print(f"\nYour level: {user_level:.2f}")
    print(f"CLO of questions answered incorrectly the most: {most_incorrect_clo}")
    advice = generate_mcqs(most_incorrect_clo).replace("**", "")
    audio_handle.audio_handler(advice, "advice.mp3")
    print(advice)


def generate_mcqs(text):
    prompt = f"the student took a quiz, and answerd some questions wrong, this is the Course Learning Outcome (CLO) of the questions that he answered wrong: {text} based on that, explain very briefly it to the student, and give advice on how to improve his level."
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a teacher"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return completion.choices[0].message.content


def main():
    json_file = r"output_questions.json"  # Replace with your JSON file path
    questions = load_questions_from_json(json_file)
    evaluate_answers(questions)


if __name__ == "__main__":
    main()
