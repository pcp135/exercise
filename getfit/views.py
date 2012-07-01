from django.shortcuts import render
from getfit.models import Workout, Score

def home(request):
	return render(request, 'home.html', {'workouts': Workout.objects.all()})
	
def workout(request, workout_id):
	context = {'workout': Workout.objects.get(pk = workout_id)}
	return render(request, 'workout.html', context)	