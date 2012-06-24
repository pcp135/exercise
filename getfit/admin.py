from django.contrib import admin
from getfit.models import *

admin.site.register(Exercise, Measure, Score, Workout)