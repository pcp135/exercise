from django.test import TestCase
from django.utils import timezone
from getfit.models import Exercise, Measure, Workout, Score
from django.core.urlresolvers import reverse
import pytz

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
		
class ViewTests(TestCase):
	def setUp(self):
		self.exer1 = Exercise(name = 'Testing')
		self.exer1.save()
		
		self.exer2 = Exercise(name = "Hitting")
		self.exer2.save()
		
		self.work1=Workout(exercise = self.exer1, time_of_workout = timezone.now())
		self.work1.save()

		self.work2=Workout(exercise = self.exer2, time_of_workout = timezone.now())
		self.work2.save()
		
		self.meas1=Measure(name = "Reps")
		self.meas1.save()
		
		self.meas2=Measure(name = "Time")
		self.meas2.save()
		
		self.exer1.measure.add(self.meas1)
		self.exer1.measure.add(self.meas2)
		self.exer2.measure.add(self.meas2)	

	def test_home_page_exists_and_uses_correct_template(self):
		response = self.client.get('/')
		template_names_used = [t.name for t in response.templates]
		self.assertIn('home.html', template_names_used)
		
	def test_home_page_displays_exercises_and_dates(self):
		response = self.client.get('/')
		self.assertIn(self.work1.exercise.name, response.content)
		self.assertIn(self.work2.exercise.name, response.content)
		self.assertIn(self.work1.time_of_workout.strftime("%A %d %B %Y"), response.content)
		self.assertIn(self.work2.time_of_workout.strftime("%A %d %B %Y"), response.content)
		
	def test_workout_page_exists_and_uses_correct_template(self):
		response = self.client.get('/workout/%d/' % self.work2.id)
		template_names_used = [t.name for t in response.templates]
		self.assertIn('workout.html', template_names_used)
		
	def test_home_page_links_to_workout_pages(self):
		response = self.client.get('/')
		work1_url = reverse('getfit.views.workout', args=[self.work1.id,])
		self.assertIn(work1_url, response.content)
		work2_url = reverse('getfit.views.workout', args=[self.work2.id,])
		self.assertIn(work2_url, response.content)
		
	def test_workout_page_lists_exercise_and_date_and_time_of_workout(self):
		response = self.client.get('/workout/%d/' % self.work2.id)
		self.assertIn(self.work2.exercise.name, response.content)
		self.assertIn(self.work2.time_of_workout.strftime("%A %d %B %Y"), response.content)
		eastern=pytz.timezone('US/Eastern')
		self.assertIn(self.work2.time_of_workout.astimezone(eastern).strftime("%H:%M"), response.content)
		
	def test_workout_lists_each_score(self):
		score1=Score(workout=self.work1, measure=self.meas1, result=2201)
		score1.save()
		score2=Score(workout=self.work1, measure=self.meas2, result=3220)
		score2.save()
		response = self.client.get('/workout/%d/' % self.work1.id)
		self.assertIn(self.meas1.name, response.content)
		self.assertIn(score2.measure.name, response.content)
		self.assertIn(str(score1.result), response.content)
		self.assertIn(u"3220", response.content)
		
		
		
		
		
