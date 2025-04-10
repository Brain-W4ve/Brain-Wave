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

class FileSummarySchema(Schema):
    """Schema for serializing file metadata summary"""
    id = fields.Int(required=True)
    filename = fields.Str(required=True)
    file_info_url = fields.Method("get_info_url")

    def get_info_url(self, obj):
        return f"http://backend:5000/file/{obj.id}"

class FileDetailSchema(Schema):
    id = fields.Int(required=True)
    filename = fields.Str(required=True)
    content_type = fields.Str(required=True)
    upload_date = fields.Str(required=True)
#     uploaded_at = fields.DateTime(attribute="upload_date", required=True)
    download_url = fields.Method("get_download_url")

    def get_download_url(self, obj):
        return f"http://backend:5000/download/{obj.id}"