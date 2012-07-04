from django import forms
from django.utils import timezone
from getfit.models import Exercise

class WorkoutScoreForm(forms.Form):
	
	def __init__(self, workout):
		forms.Form.__init__(self)
		for score in workout.score_set.all():
			self.fields[score.measure.name] = forms.DecimalField(initial = score.result)

class NewWorkoutForm(forms.Form):
	exercise = forms.ChoiceField()
	time_of_workout = forms.DateTimeField()

	def __init__(self):
		forms.Form.__init__(self)
		self.fields['exercise'].choices = [(ex.id, ex.name) for ex in Exercise.objects.all()]
		self.fields['time_of_workout'].initial =  timezone.now()