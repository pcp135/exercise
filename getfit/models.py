from django.db import models

class Measure(models.Model):
	name = models.CharField(max_length=100)
	
class Exercise(models.Model):
	name = models.CharField(max_length=100)
	measure = models.ManyToManyField(Measure)
	
class Workout(models.Model):
	exercise = models.ForeignKey(Exercise)
	time_of_workout = models.DateTimeField()
	
class Score(models.Model):
	workout = models.ForeignKey(Workout)
	measure = models.ForeignKey(Measure)
	result = models.IntegerField()
