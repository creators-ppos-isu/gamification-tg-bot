from tortoise import models, fields


class User(models.Model): 
    id = fields.IntField(pk=True)