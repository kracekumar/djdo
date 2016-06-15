import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

def add_default_due_date():
    return timezone.now() + datetime.timedelta(days=1)


class Todo(models.Model):
    name = models.CharField(max_length=255, unique=True)
    notes = models.TextField()
    is_completed = models.BooleanField(db_index=True)
    due_date = models.DateTimeField(default=add_default_due_date)

    def __str__(self):
        return "<id: {}, name: {}, is_completed: {}, due_date: {}>".format(self.id, self.name, self.is_completed, self.due_date)
