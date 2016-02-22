from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
	user = models.ForeignKey(User)
	addressLine1 = models.TextField()
	addressLine2 = models.TextField()
	state = models.TextField()
	city = models.TextField()
	pinNo = models.IntegerField()
	mobileNo = models.IntegerField()
