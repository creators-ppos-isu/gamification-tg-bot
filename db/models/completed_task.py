from tortoise.models import Model
from tortoise import fields


class CompletedTask(Model):
    user = fields.ForeignKeyField('models.User')
    task = fields.ForeignKeyField('models.Task')
    score = fields.IntField()