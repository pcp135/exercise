from django import forms
from django.utils import timezone
from getfit.models import Workout, Measure, Exercise
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
	time_of_workout = forms.DateField(widget=widgets.AdminDateWidget)
	
	class Meta:
		model = Workout

class NewMeasureForm(forms.ModelForm):
	class Meta:
		model = Measure

class NewExerciseForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
	        super(NewExerciseForm, self).__init__(*args, **kwargs)
	        self.fields['measure'].help_text = ""
	
	class Meta:
		model = Exercise
		widgets = {'measure': forms.CheckboxSelectMultiple}
		help_text = {'measure': ""}
	
		