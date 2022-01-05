from django.db import models
from authentication.models import User
from helpers.models import TrackingModel

# Create your models here.
class Todo(TrackingModel):
	user_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=225)
	is_primary = models.BooleanField(default=False)
	owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name
