from marshmallow import Schema, fields



class User_Schema(Schema):
    id = fields.Integer()
    email = fields.String()
    username = fields.String()
    password_hash = fields.String()
    # files = 
    # reports