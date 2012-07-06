from django import forms
from django.utils import timezone
from getfit.models import Workout

class WorkoutScoreForm(forms.Form):
	
	def __init__(self, workout):
		forms.Form.__init__(self)
		for score in workout.score_set.all():
			self.fields[score.measure.name] = forms.DecimalField(initial = score.result)

class NewWorkoutForm(forms.ModelForm):
	class Meta:
		model = Workout
