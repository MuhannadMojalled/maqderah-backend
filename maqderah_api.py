import os
from flask import Flask, request, jsonify
import generate_questions

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".pdf"):
        # Ensure the uploads directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        global file_path
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return jsonify({"message": "File successfully uploaded"}), 200

    return jsonify({"error": "Invalid file format. Only PDFs are allowed"}), 400


@app.route("/get-quetsions", methods=["GET"])
def getQuestions():
    return generate_questions.generateQuestions(file_path)


if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)
