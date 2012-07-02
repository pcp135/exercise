from django import forms

class WorkoutScoreForm(forms.Form):
	
	def __init__(self, workout):
		forms.Form.__init__(self)
		for score in workout.score_set.all():
			self.fields[score.measure.name] = forms.DecimalField(initial = score.result)
