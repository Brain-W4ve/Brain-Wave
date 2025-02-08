from flask import Flask, request, jsonify
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
                    {"name": "attack1", "start": 8121, "finish": 8129},
                    {"name": "attack2", "start": 8281, "finish": 8289},
                    {"name": "attack3", "start": 8389, "finish": 8400},
                    {"name": "attack4", "start": 8623, "finish": 8630},
                    {"name": "attack5", "start": 8701, "finish": 8709},
                    {"name": "attack6", "start": 8774, "finish": 8784},
                    {"name": "attack7", "start": 8864, "finish": 8872},
                    {"name": "attack8", "start": 9012, "finish": 9027},
                    {"name": "attack9", "start": 9337, "finish": 9352},
                    {"name": "attack10", "start": 9689, "finish": 9704},
                    {"name": "attack11", "start": 10070, "finish": 10073},
                    {"name": "attack12", "start": 10992, "finish": 11022},
                    {"name": "attack13", "start": 11120, "finish": 11132},
                    {"name": "attack14", "start": 11210, "finish": 11218},
                    {"name": "attack15", "start": 11220, "finish": 11234},
                    {"name": "attack16", "start": 11409, "finish": 11420},
                    {"name": "attack17", "start": 11425, "finish": 11436},
                    {"name": "attack18", "start": 11521, "finish": 11542},
                    {"name": "attack19", "start": 11606, "finish": 11613},
                    {"name": "attack20", "start": 11617, "finish": 11632},
                    {"name": "attack21", "start": 11710, "finish": 11734},
                    {"name": "attack22", "start": 11812, "finish": 11836},
                    {"name": "attack23", "start": 11918, "finish": 11944},
                    {"name": "attack24", "start": 12044, "finish": 12058},
                    {"name": "attack25", "start": 12130, "finish": 12156},
                    {"name": "attack26", "start": 12242, "finish": 12250},
                    {"name": "attack27", "start": 12254, "finish": 12266},
                    {"name": "attack28", "start": 12352, "finish": 12362},
                    {"name": "attack29", "start": 12366, "finish": 12382},
                    {"name": "attack30", "start": 12480, "finish": 12494},
                    {"name": "attack31", "start": 12570, "finish": 12598},
                    {"name": "attack32", "start": 12688, "finish": 12701},
                    {"name": "attack33", "start": 12786, "finish": 12796},
                    {"name": "attack34", "start": 12818, "finish": 12846},
                    {"name": "attack35", "start": 12918, "finish": 12927},
                    {"name": "attack36", "start": 12929, "finish": 12944},
                    {"name": "attack37", "start": 13038, "finish": 13046},
                    {"name": "attack38", "start": 13049, "finish": 13064},
                    {"name": "attack39", "start": 13080, "finish": 13092},
                    {"name": "attack40", "start": 13190, "finish": 13204},
                    {"name": "attack41", "start": 13588, "finish": 13613}
                ]
            }
            for channel in file.channels
        ]

        return jsonify({"filename": file.filename, "channels": channels})

if __name__ == "__main__":
    app.run(debug=True)