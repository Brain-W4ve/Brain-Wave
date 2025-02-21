from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from .models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .preprocessing import apply_median_filter
from dotenv import load_dotenv
import bioread
import json
import os
import io
from statistics import mean
import tempfile

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
            file_content = io.BytesIO(file.read())
            data = bioread.read_file(file_content)
            new_file_data = File_Data(filename=file.filename)
            for i, channel in enumerate(data.channels):
                processed_data = apply_median_filter(channel.data)
                channel_data = Channel_Data(
                    channel_number=i,
                    sampling_rate=channel.samples_per_second,
                    data=json.dumps(processed_data.tolist())
                )
                new_file_data.channels.append(channel_data)

            session.add(new_file_data)
            session.commit()
            return jsonify({
                "success": f"File: {file.name} processed and saved successfully",
                "fileId": new_file_data.id
            }), 200

        except Exception as e:
            session.rollback()
            return jsonify({"error": f"Error processing file: {str(e)}"}), 400

@app.route("/files/<int:file_id>/channels", methods=["GET"])
def get_file_channels(file_id):
    with Session(engine) as session:
        file = session.query(File_Data).filter(File_Data.id == file_id).first()
        if not file:
            return jsonify({"error": "File not found"}), 404
        
        channels = [
            {
                "channelNumber": channel.channel_number,
                "samplingRate": channel.sampling_rate,
                "dataLength": len(json.loads(channel.data)),  # Return the length of data, not full data
                "data": json.loads(channel.data),
                "attacks": [
                ]
            }
            for channel in file.channels
        ]

        return jsonify({"filename": file.filename, "channels": channels})

@app.route("/files/<int:file_id>/report", methods=["GET"])
def get_report(file_id):
    response = get_file_channels(file_id)
    
    if response.status_code != 200:
        return response

    data = response.get_json()
    channels = data["channels"]

    report = {
        "filename": data["filename"],
        "totalChannels": len(channels),
        "averageSamplingRate": mean(channel["samplingRate"] for channel in channels),
        "totalDataLength": sum(channel["dataLength"] for channel in channels),
        "attacksPerChannel": [
            {
                "channelNumber": channel["channelNumber"],
                "totalAttacks": len(channel["attacks"]),
                "attackDurations": sum(attack["finish"] - attack["start"] for attack in channel["attacks"])
            }
            for channel in channels
        ]
    }

    # Save report as a temporary JSON file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        json.dump(report, temp_file, indent=4)
        temp_file_path = temp_file.name

    # Send the file and remove it afterward
    response = send_file(temp_file_path, as_attachment=True)
    os.remove(temp_file_path)
    return response


if __name__ == "__main__":
    app.run(debug=True)