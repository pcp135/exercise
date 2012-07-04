from django.shortcuts import render
from getfit.models import Workout, Score, Exercise
from getfit.forms import WorkoutScoreForm, NewWorkoutForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def home(request):
	return render(request, 'home.html', {'workouts': Workout.objects.all()})
	
def workout(request, workout_id):
	workout = Workout.objects.get(pk = workout_id)
	if request.method == 'POST':
		for score in workout.score_set.all():
			score.result=request.POST[score.measure.name]
			score.save()
		return HttpResponseRedirect(reverse('getfit.views.workout', args=[workout_id,]))
	
	form = WorkoutScoreForm(workout)
	context = {'workout': workout, 'form': form}
	return render(request, 'workout.html', context)	
	
def add(request):
	if request.method == 'POST':
		workout=Workout()
		workout.exercise=Exercise.objects.get(id = request.POST['exercise'])
		workout.time_of_workout = request.POST['time_of_workout']
		workout.save()
		for meas in workout.exercise.measure.all():
			score = Score(workout=workout, measure=meas, result=0)
			score.save()
		return HttpResponseRedirect(reverse('getfit.views.workout', args=[workout.id,]))
	
	form = NewWorkoutForm()
	return render(request, 'add.html', {'form': form})
