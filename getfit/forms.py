from django import forms
from django.utils import timezone
from getfit.models import Workout
from django.contrib.admin import widgets                                       

class WorkoutScoreForm(forms.Form):
	
	def __init__(self, workout, post_data=None):
		forms.Form.__init__(self, post_data)
		for score in workout.score_set.all():
			if post_data is None:
				self.fields[score.measure.name] = forms.DecimalField(initial = score.result)
			else:
				self.fields[score.measure.name] = forms.DecimalField()

class NewWorkoutForm(forms.ModelForm):
	time_of_workout = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime)
	
	class Meta:
		model = Workout
