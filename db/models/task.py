from tortoise.models import Model
from tortoise import fields


class Task(Model): 
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    score = fields.IntField()

    def __str__(self) -> str:
        return f'{self.title}: {self.score} баллов'
    

async def create_default_tasks(): 
    tasks = [
        Task(id=1, title='Вовремя прийти на лекции', score=1),
        Task(id=2, title='Активное участие в Мастер-классе', score=1),
        Task(id=3, title='История с мероприятия', score=1),
        Task(id=4, title='Вопросы на лекции', score=2),
        Task(id=5, title='Доп. баллы', score=2),
        Task(id=6, title='Баллы от лектора', score=2),
    ]
    for task in tasks:
        if not await Task.exists(id=task.id):
            await task.save()