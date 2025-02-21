from marshmallow import Schema, fields, validate, post_load
from models.user import User

class ReportSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.String(required=True)
    generated_date = fields.DateTime(dump_only=True)
    file_id = fields.Int(required=True)
    user_id = fields.Int(dump_only=True)


class FileSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.String(required=True)
    upload_date = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    reports = fields.Nested(ReportSchema, many=True, exclude=('file_id',))


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=255))
    password = fields.String(required=True, validate=validate.Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'))


    files = fields.Nested(FileSchema, many=True, dump_only=True)
    reports = fields.Nested(ReportSchema, many=True, dump_only=True)

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data) 