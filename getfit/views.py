from django.shortcuts import render
from getfit.models import Workout, Score
from getfit.forms import WorkoutScoreForm

def home(request):
	return render(request, 'home.html', {'workouts': Workout.objects.all()})
	
def workout(request, workout_id):
	workout = Workout.objects.get(pk = workout_id)
	form = WorkoutScoreForm(workout)
	context = {'workout': workout, 'form': form}
	return render(request, 'workout.html', context)	