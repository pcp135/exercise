from django.shortcuts import render
from getfit.models import Workout, Score, Exercise, Measure
from getfit.forms import WorkoutScoreForm, NewWorkoutForm, NewMeasureForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
import pytz

def home(request):
	return render(request, 'home.html', {'workouts': Workout.objects.all().order_by('-time_of_workout'), 'home_active': "active"})
	
def workout(request, workout_id):
	try:
		workout = Workout.objects.get(pk = workout_id)
	except:
		workout = None
	if workout:
		if request.method == 'POST':
			form = WorkoutScoreForm(workout, request.POST)
			if form.is_valid():
				for score in workout.score_set.all():
					score.result=request.POST[score.measure.name]
					score.save()
				return HttpResponseRedirect(reverse('getfit.views.home'))
		else:
			form = WorkoutScoreForm(workout)
		context = {'workout': workout, 'form': form}
		return render(request, 'workout.html', context)	
	else:
		return render(request, 'invalidworkout.html')
	
def add(request):
	if request.method == 'POST':
		form = NewWorkoutForm(request.POST)
		if form.is_valid():
			workout=form.save()
			for meas in workout.exercise.measure.all():
				Score(workout=workout, measure=meas, result=0).save()
			return HttpResponseRedirect(reverse('getfit.views.workout', args=[workout.id,]))
	else:
		form = NewWorkoutForm()		
	return render(request, 'add.html', {'form': form, 'type': "New", 'action': "Add", 'add_active': "active"})
	
def delete(request, workout_id):
	try:
		workout = Workout.objects.get(pk = workout_id)
	except:
		workout = None
	if workout:
		workout.delete()
		return HttpResponseRedirect(reverse('getfit.views.home'))
	else:
		return render(request, 'invalidworkout.html')
		
def edit(request, workout_id):
	try:
		workout = Workout.objects.get(pk = workout_id)
	except:
		workout = None
	if workout:
		if request.method == 'POST':
			form = NewWorkoutForm(request.POST)
			if form.is_valid():
				workout.exercise = form.cleaned_data['exercise']
				workout.time_of_workout = form.cleaned_data['time_of_workout']
				workout.save()
				return HttpResponseRedirect(reverse('getfit.views.workout', args=[workout.id,]))
		else:
			eastern=pytz.timezone('US/Eastern')
			form = NewWorkoutForm({'exercise': workout.exercise.id, 'time_of_workout_0': workout.time_of_workout.astimezone(eastern).strftime('%Y-%m-%d'), 'time_of_workout_1': workout.time_of_workout.astimezone(eastern).strftime('%H:%M')})
			return render(request, 'add.html', {'form': form, 'type': "Edit", 'action': "Update"})
	else:
		return render(request, 'invalidworkout.html')
		
def measures(request):
	return render(request, 'measures.html', {'measures': Measure.objects.all(), 'measure_active': 'active'})

def addmeasure(request):
	if request.method == 'POST':
		form = NewMeasureForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('getfit.views.measures'))
	else:
		form = NewMeasureForm()		
	return render(request, 'addmeasures.html', {'form': form})
