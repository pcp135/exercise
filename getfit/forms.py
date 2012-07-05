from django import forms
from django.utils import timezone
from getfit.models import Exercise

class WorkoutScoreForm(forms.Form):
	
	def __init__(self, workout):
		forms.Form.__init__(self)
		for score in workout.score_set.all():
			self.fields[score.measure.name] = forms.DecimalField(initial = score.result)

class NewWorkoutForm(forms.Form):
	exercise = forms.ChoiceField(choices = [(0,"----")]+[(ex.id, ex.name) for ex in Exercise.objects.all()])
	time_of_workout = forms.DateTimeField()