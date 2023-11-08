from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=32, null=True)
    last_name = fields.CharField(max_length=32, null=True)
    is_admin = fields.BooleanField(default=False)
    score = fields.IntField(default=0)

    def __str__(self): 
        return f'{self.first_name} {self.last_name}'