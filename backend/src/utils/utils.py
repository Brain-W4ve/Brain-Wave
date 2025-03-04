from marshmallow import ValidationError, Schema
from flask import jsonify

def validate_schema(schema: Schema, data: dict):
    try:
        return schema.load(data), None
    except ValidationError as err:
        return None, jsonify({
            "status": "fail",
            "errors": err.messages
        })