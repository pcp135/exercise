from django.contrib import admin
from getfit.models import *

class ScoreInline(admin.TabularInline):
	model = Score
	extra = 4
	
class WorkoutAdmin(admin.ModelAdmin):
	inlines = [ScoreInline]

admin.site.register(Exercise)
admin.site.register(Workout, WorkoutAdmin)