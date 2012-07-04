from django.db import models

class Measure(models.Model):
	name = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.name
	
class Exercise(models.Model):
	name = models.CharField(max_length=100)
	measure = models.ManyToManyField(Measure)
	
	def __unicode__(self):
		return self.name
	
class Workout(models.Model):
	exercise = models.ForeignKey(Exercise)
	time_of_workout = models.DateTimeField()
	
	def __unicode__(self):
		return self.exercise.name + " @ " + str(self.time_of_workout)
	
class Score(models.Model):
	workout = models.ForeignKey(Workout)
	measure = models.ForeignKey(Measure)
	result = models.DecimalField(decimal_places=2, max_digits=10)
	
	def __unicode__(self):
		return str(self.result) + " " + self.measure.name
