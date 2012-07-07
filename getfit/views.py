from django.shortcuts import render
from getfit.models import Workout, Score, Exercise
from getfit.forms import WorkoutScoreForm, NewWorkoutForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
import pytz

def home(request):
	return render(request, 'home.html', {'workouts': Workout.objects.all()})
	
def workout(request, workout_id):
	workout = Workout.objects.get(pk = workout_id)
	if request.method == 'POST':
		for score in workout.score_set.all():
			score.result=request.POST[score.measure.name]
			score.save()
		return HttpResponseRedirect(reverse('getfit.views.home'))
	
	form = WorkoutScoreForm(workout)
	context = {'workout': workout, 'form': form}
	return render(request, 'workout.html', context)	
	
def add(request):
	if request.method == 'POST':
		form = NewWorkoutForm(request.POST)
		if form.is_valid():
			workout=form.save()
			for meas in workout.exercise.measure.all():
				Score(workout=workout, measure=meas, result=0).save()
			return HttpResponseRedirect(reverse('getfit.views.workout', args=[workout.id,]))
	else:
		eastern=pytz.timezone('US/Eastern')
		form = NewWorkoutForm({'exercise': 1, 'time_of_workout': str(timezone.now().astimezone(eastern).strftime('%Y-%m-%d %H:%M'))})		
	return render(request, 'add.html', {'form': form})
	
def delete(request, workout_id):
	workout = Workout.objects.get(pk = workout_id)
	workout.delete()
	return HttpResponseRedirect(reverse('getfit.views.home'))
