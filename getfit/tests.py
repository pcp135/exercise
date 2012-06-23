from django.test import TestCase
from django.utils import timezone
from getfit.models import Exercise, Measure

class SimpleTest(TestCase):
	def test_basic_addition(self):
		"""
		Tests that 1 + 1 always equals 2.
		"""
		self.assertEqual(1 + 1, 2)

class ModelTests(TestCase):
	def setUp(self):
		self.exercise = Exercise()
		self.exercise.name = "Test exercise"
		self.exercise.save()
		
		self.meas = Measure()
		self.meas.name = "Reps"
		self.meas.save()
		
	def test_creating_a_new_exercise(self):
		all_exercises = Exercise.objects.all()
		self.assertEquals(len(all_exercises),1)
		
		self.assertEquals(self.exercise, all_exercises[0])
		
		self.assertEquals(all_exercises[0].name, "Test exercise")
		
	def test_creating_a_new_measure(self):
		all_measures = Measure.objects.all()
		self.assertEquals(len(all_measures),1)
		
		self.assertEquals(self.meas, all_measures[0])
		
		self.assertEquals(all_measures[0].name, "Reps")