from marshmallow import Schema, fields, ValidationError, validates
from flask import request
from enum import Enum
from werkzeug.datastructures import FileStorage

class ALLOWED_EXTENSIONS(Enum):
    PNG = "png"
    JPG = "jpg"
    PDF = "pdf"
    TXT = "txt"
    ACQ = "acq"

ALLOWED_EXTENSIONS_SET = {e.value for e in ALLOWED_EXTENSIONS}

def validate_file_type(file: FileStorage) -> None:
    """Ensure only specific file types are allowed"""
    if "." not in file.filename:
        raise ValidationError("Invalid file format. No extension found.")
    
    ext = file.filename.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS_SET:
        raise ValidationError(f"Invalid file type. Allowed types are: {', '.join(ALLOWED_EXTENSIONS_SET)}")

class FileUploadSchema(Schema):
    """Schema for validating and serializing file uploads"""
    file = fields.Raw(required=True)

    @validates("file")
    def validate_file(self, file):
        validate_file_type(file)

class FileMetadataSchema(Schema):
    """Schema for serializing file metadata"""
    id = fields.Int(required=True)
    filename = fields.Str(required=True)
    content_type = fields.Str(required=True)
    download_url = fields.Str(required=True)
    uploaded_at = fields.DateTime(required=True)