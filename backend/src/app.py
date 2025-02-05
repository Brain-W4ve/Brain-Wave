from flask import Flask, request, jsonify
from flask_cors import CORS
from .models.file_data import File_Data
from .models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .preprocessing import apply_median_filter
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

engine = create_engine(os.getenv("DATABSE_URL", "sqlite:///data.db"), future=True)
Base.metadata.create_all(engine)

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    with Session(engine) as session:
        try:
            file_content = file.read()
            # processed_data = apply_median_filter(file_content)
            new_file_data = File_Data(filename=file.filename, data=file_content)
            session.add(new_file_data)
            session.commit()
            return jsonify({"success": f"File: {file.name} processed and saved successfully"}), 200

        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error processing file: {str(e)}"}), 400


if __name__ == "__main__":
    app.run(debug=True)