from django.test import TestCase
from django.utils import timezone
from getfit.models import Exercise

class SimpleTest(TestCase):
	def test_basic_addition(self):
		"""
		Tests that 1 + 1 always equals 2.
		"""
		self.assertEqual(1 + 1, 2)

class ExerciseTest(TestCase):
	def test_creating_a_new_exercise(self):
		exercise = Exercise()
		exercise.name = "Test exercise"
		exercise.reps = 10
		exercise.save()
		
		all_exercises = Exercise.objects.all()
		self.assertEquals(len(all_exercises),1)
		
		self.assertEquals(exercise, all_exercises[0])
		
		self.assertEquals(all_exercises[0].name, "Test exercise")
		self.assertEquals(all_exercises[0].reps, 10)