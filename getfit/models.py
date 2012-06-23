from django.db import models

class Exercise(models.Model):
	name = models.CharField(max_length=100)
	
class Measure(models.Model):
	name = models.CharField(max_length=100)
	exercise = models.ManyToManyField(Exercise)
	
class Workout(models.Model):
	exercise = models.ForeignKey(Exercise)
	time_of_workout = models.DateTimeField()
	
class Score(models.Model):
	workout = models.ForeignKey(Workout)
	measure = models.ForeignKey(Measure)
	result = models.IntegerField()
