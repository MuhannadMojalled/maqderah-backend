import json


# Parse the MCQs text generated by OpenAI
def parse_mcqs(mcqs_text):
    questions = []
    summary = mcqs_text.split("### Questions")[0].strip()
    mcqs_list = mcqs_text.split("### Questions")[1].strip().split("\n\n")

    for mcq in mcqs_list:
        if mcq.strip():
            parts = mcq.split("\n")
            question = parts[0].strip()
            options = [
                parts[1].strip(),
                parts[2].strip(),
                parts[3].strip(),
                parts[4].strip(),
            ]
            correct_answer = parts[5].split(":")[1].strip()
            clo = parts[6].split(":")[1].strip()
            difficulty = parts[7].split(":")[1].strip()
            questions.append(
                {
                    "question": question,
                    "options": options,
                    "correct_answer": correct_answer,
                    "clo": clo,
                    "difficulty": difficulty,
                }
            )
    summary = summary.replace("### Summary\n", "")
    return {"summary": summary, "questions": questions}


def save_as_json(questions, output_path):
    formatted_questions = []
    for idx, question_data in enumerate(questions["questions"], start=1):
        question = question_data["question"].replace("**", "")  # Remove ** markers
        question = question.split(".")[1].strip()  # Remove number and dot
        options = question_data["options"]
        correct_answer = (
            question_data["correct_answer"].replace(" ", "").replace("**", "")
        )
        correct_answer = (
            question_data["correct_answer"].replace(" ", "").replace("**", "")
        )
        difficulty = question_data["difficulty"].replace("**", "").replace(" ", "")
        clo = question_data["clo"].replace("**", "")

        # Map options to A, B, C, D
        answers = {"A": options[0], "B": options[1], "C": options[2], "D": options[3]}

        # Create the formatted question structure
        formatted_question = {
            "question": {"questionNumber": str(idx), "question": question},
            "answers": answers,
            "correct_answer": correct_answer,
            "clo": clo,
            "difficulty": difficulty,
        }

        formatted_questions.append(formatted_question)
    formatted_data = {"summary": questions["summary"], "questions": formatted_questions}

    # Write to JSON file
    with open(output_path, "w") as f:
        json.dump(formatted_data, f, indent=4)
    return formatted_data
