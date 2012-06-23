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
		self.exer = Exercise()
		self.exer.name = "Test exercise"
		self.exer.save()
		
		self.meas = Measure()
		self.meas.name = "Reps"
		self.meas.save()
		self.meas.exercise.add(self.exer)

		self.meas2 = Measure()
		self.meas2.name = "Height"
		self.meas2.save()
		self.meas2.exercise.add(self.exer)

		self.exer2 = Exercise()
		self.exer2.name = "Jumping"
		self.exer2.save()		
		self.meas2.exercise.add(self.exer2)
		
	def test_creating_a_new_exercise(self):
		all_exercises = Exercise.objects.all()
		self.assertEquals(len(all_exercises),2)
		
		self.assertEquals(self.exer, all_exercises[0])
		
		self.assertEquals(all_exercises[0].name, "Test exercise")
		
	def test_creating_a_new_measure(self):
		all_measures = Measure.objects.all()
		self.assertEquals(len(all_measures),2)
		
		self.assertEquals(self.meas, all_measures[0])
		
		self.assertEquals(all_measures[0].name, "Reps")
		self.assertEquals(all_measures[0].exercise.all()[0], self.exer)
		self.assertEquals(all_measures[0].exercise.all()[0].name, "Test exercise")
		
	def test_exercise_knows_its_measures(self):
		measures = [v.name for v in self.exer.measure_set.all()]
		
		self.assertIn("Reps", measures)
		self.assertIn("Height", measures)

		measures = [v.name for v in self.exer2.measure_set.all()]
		
		self.assertNotIn("Reps", measures)
		self.assertIn("Height", measures)
