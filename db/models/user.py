from tortoise.models import Model
from tortoise import fields
from tortoise.exceptions import ValidationError


def validate_name(name: str):
    if name.isdigit():
        raise ValidationError('Имя или фамилия не может быть числом')


class User(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=32, null=True, validators=[validate_name])
    last_name = fields.CharField(max_length=32, null=True, validators=[validate_name])
    is_admin = fields.BooleanField(default=False)
    score = fields.IntField(default=0)

    completed_task = fields.ManyToManyField('models.Task')

    def __str__(self): 
        return f'{self.first_name} {self.last_name}'
