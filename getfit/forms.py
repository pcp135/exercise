from django import forms
from django.utils import timezone
from getfit.models import Workout

class WorkoutScoreForm(forms.Form):
	
	def __init__(self, workout, post_data=None):
		forms.Form.__init__(self, post_data)
		for score in workout.score_set.all():
			if post_data is None:
				self.fields[score.measure.name] = forms.DecimalField(initial = score.result)
			else:
				self.fields[score.measure.name] = forms.DecimalField()

class NewWorkoutForm(forms.ModelForm):
	class Meta:
		model = Workout
