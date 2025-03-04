from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))
    username = fields.String(required=True, validate=validate.Length(max=255))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email()
    username = fields.String()