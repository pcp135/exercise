from django.test import TestCase
from django.utils import timezone
from getfit.models import Exercise, Measure, Workout, Score

class ModelTests(TestCase):
	def setUp(self):
		self.meas = Measure()
		self.meas.name = "Reps"
		self.meas.save()
		
		self.meas2 = Measure()
		self.meas2.name = "Height"
		self.meas2.save()
		
		self.exer = Exercise()
		self.exer.name = "Test exercise"
		self.exer.save()
		self.exer.measure.add(self.meas)
		self.exer.measure.add(self.meas2)
		
		self.exer2 = Exercise()
		self.exer2.name = "Jumping"
		self.exer2.save()		
		self.exer2.measure.add(self.meas2)
		
		self.work = Workout()
		self.worktime = timezone.now()
		self.work.time_of_workout = self.worktime
		self.work.exercise = self.exer
		self.work.save()
		
		self.score = Score()
		self.score.workout = self.work
		self.score.measure = self.meas
		self.score.result = 10
		self.score.save()

		self.score2 = Score()
		self.score2.workout = self.work
		self.score2.measure = self.meas2
		self.score2.result = 20
		self.score2.save()
		
	def test_creating_a_new_exercise(self):
		all_exercises = Exercise.objects.all()
		self.assertEquals(len(all_exercises),2)
		
		self.assertEquals(self.exer, all_exercises[0])
		
		self.assertEquals(all_exercises[0].name, "Test exercise")
		self.assertEquals(all_exercises[0].measure.all()[0].name, "Reps")
		self.assertEquals(all_exercises[0].measure.all()[0], self.meas)
		
	def test_creating_a_new_measure(self):
		all_measures = Measure.objects.all()
		self.assertEquals(len(all_measures),2)
		
		self.assertEquals(self.meas, all_measures[0])
		
		self.assertEquals(all_measures[0].name, "Reps")
		
	def test_exercise_knows_its_measures(self):
		measures = [v.name for v in self.exer.measure.all()]
		
		self.assertIn("Reps", measures)
		self.assertIn("Height", measures)

		measures = [v.name for v in self.exer2.measure.all()]
		
		self.assertNotIn("Reps", measures)
		self.assertIn("Height", measures)
		
	def test_creating_a_new_workout(self):
		all_workouts = Workout.objects.all()
		self.assertEquals(len(all_workouts),1)
		
		self.assertEquals(self.work, all_workouts[0])
		self.assertEquals("Test exercise", all_workouts[0].exercise.name)
		self.assertEquals(self.worktime, all_workouts[0].time_of_workout)
		
	def test_adding_a_new_score(self):
		all_scores = Score.objects.all()
		self.assertEquals(len(all_scores),2)

		self.assertEquals(self.score, all_scores[0])
		self.assertEquals("Test exercise", all_scores[0].workout.exercise.name)
		self.assertEquals("Reps", all_scores[0].measure.name)
		self.assertEquals(10, all_scores[0].result)

		self.assertEquals(self.score2, all_scores[1])
		self.assertEquals("Test exercise", all_scores[1].workout.exercise.name)
		self.assertEquals("Height", all_scores[1].measure.name)
		self.assertEquals(20, all_scores[1].result)
		
	def test_objects_should_have_unicode_output(self):
		self.assertEquals(u"Test exercise", unicode(self.exer))
		self.assertEquals(u"Reps", unicode(self.meas))
		self.assertEquals(u"Test exercise @ " + str(self.worktime), unicode(self.work))
		self.assertEquals(u"10 Reps", unicode(self.score))
		
