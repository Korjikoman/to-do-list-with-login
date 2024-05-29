from django.db import models
from django.utils import timezone
# Create your models here.
class Task(models.Model):
	title = models.CharField(max_length=200)
	complete = models.BooleanField(default=False)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title
