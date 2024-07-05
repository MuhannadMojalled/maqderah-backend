import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import pdf_handler
import output_handler


def generateQuestions(filepath):
    output_json_path = "output_questions.json"
    # load environment variables
    _ = load_dotenv(find_dotenv())
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    model = "gpt-4o"
    temperature = 0.3
    max_tokens = 1000

    # generate multiple-choice questions
    def generate_mcqs(text, num_questions=10):
        prompt = f"Create {num_questions} multiple-choice questions, and summarize the text very breifly and choose a Course Learning Outcome (CLOs) for each question based on the question and I want you to use only three different CLOs, also assign each question a difficulty. only using the following text:\n\n{text}\n\nFormat: summary, Question, four options (A, B, C, D), and the correct answer as the letter (A, B, C, D), and the CLO, and a difficulty as a number in range of 10."
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    # Main function
    def main(pdf_path, output_json_path):
        text = pdf_handler.extract_text_from_pdf(pdf_path)
        mcqs_text = generate_mcqs(text)
        questions = output_handler.parse_mcqs(mcqs_text)
        questions = output_handler.save_as_json(questions, output_json_path)
        return questions

    return main(filepath, output_json_path)
