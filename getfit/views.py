from django.shortcuts import render
from getfit.models import Workout

def home(request):
	return render(request, 'home.html', {'workouts': Workout.objects.all()})