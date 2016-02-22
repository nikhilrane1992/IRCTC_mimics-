from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
	user = models.ForeignKey(User)
	addressLine1 = models.TextField()
	addressLine2 = models.TextField()
	state = models.TextField()
	city = models.TextField()
	pinNo = models.IntegerField()
	mobileNo = models.TextField()


class Location(models.Model): ## if we want we can take lat, lng here
	locationText = models.CharField(max_length=50)
	arrivalTime = models.TimeField(null=True)
	departureTime = models.TimeField(null=True)
	stationName = models.CharField(max_length=100)
	isLastStop = models.BooleanField(default=False)
	isFirstStop = models.BooleanField(default=False)

class Train(models.Model):
	trainNo = models.IntegerField()
	trainName = models.CharField(max_length=100)
	def __unicode__(self):
		return self.trainName

class Station(models.Model):
	location = models.ForeignKey('Location')
	train = models.ForeignKey('Train')

	def __unicode__(self):
		return self.stationName

class DepartureDay(models.Model):
	MONDAY = 0
	TUESDAY = 1
	WEDNESDAY = 2
	THURSDAY = 3
	FRIDAY = 4
	SATURDAY = 5
	SUNDAY = 6

	WEEKDAYCHOICES = ((MONDAY, "Monday"), (TUESDAY, "Tuesday"), (WEDNESDAY, "Wednesday"), (THURSDAY, "Thursday"), (FRIDAY, "Friday"), (SATURDAY, "Saturday"), (SUNDAY, "Sunday"))
	depDay = models.IntegerField(choices=WEEKDAYCHOICES)
	train = models.ForeignKey('Train')

class Reservation(models.Model):
	MALE = 0
	FEMALE = 1
	GENDERCHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

	userDetail = models.ForeignKey('UserDetail')
	firstName = models.CharField(max_length=30)
	lastName = models.CharField(max_length=50)
	gender = models.IntegerField(choices=GENDERCHOICES)
	age = models.IntegerField()
	addressLine1 = models.TextField()
	addressLine2 = models.TextField()
	state = models.TextField()
	city = models.TextField()
	pinNo = models.IntegerField()
	mobileNo = models.TextField()
	pnrNo = models.TextField()
	journeyDate = models.DateTimeField()
	coachAndSeatNo = models.TextField() 
	source = models.ForeignKey('Location',related_name='source')
	destination = models.ForeignKey('Location',related_name='destination')
	train = models.ForeignKey('Train')
	def __unicode__(self):
		return self.firstName
