from flask import Blueprint, request, jsonify
from models import *
from sqlalchemy.orm import Session
import io
import bioread
from app import engine
from preprocessing import apply_median_filter
import json
from marshmallow import Schema, fields

file_bp = Blueprint('file_management', __name__)

@file_bp.route("/upload", methods=["POST"])
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

@file_bp.route("/files", methods=["GET"])
def get_files():
    with Session(engine) as session:
        files = session.query(File_Data).all()
        schema = File_Data_Schema(many=True)
        return jsonify(schema.dump(files))
    
@file_bp.route("/files/<int:file_id>/data")
def get_file_data():
    ...

@file_bp.route("/files/<int:file_id>", methods=["GET"])
def get_file_details():
    ...

@file_bp.route("/files/<int:file_id>/report", methods=["GET"])
def download_report():
    ...


# I believe this should be get_file_data
@file_bp.route("/files/<int:file_id>", methods=["GET"])
def file_details(register_id):
    with Session(engine) as session:
        file = session.query(File_Data).filter(File_Data.id == register_id).first()
        if not file:
            return jsonify({"error": "File not found"}), 404
        
        channels = [
            {
                "channelNumber": channel.channel_number,
                "samplingRate": channel.sampling_rate,
                "dataLength": len(json.loads(channel.data)),  # Return the length of data, not full data
                "data": json.loads(channel.data),
                "attacks": [
                    {"name": "attack1", "start": 200, "finish": 205},
                    {"name": "attack2", "start": 368, "finish": 372}
                ]
            }
            for channel in file.channels
        ]

        return jsonify({"filename": file.filename, "channels": channels})