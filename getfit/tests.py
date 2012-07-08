from django.test import TestCase
from django.utils import timezone
from getfit.models import Exercise, Measure, Workout, Score
from getfit.forms import WorkoutScoreForm, NewWorkoutForm
from django.core.urlresolvers import reverse
from datetime import timedelta
import pytz

class ModelTests(TestCase):
	def setUp(self):
		self.eastern=pytz.timezone('US/Eastern')
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
		self.eastern=pytz.timezone('US/Eastern')
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

		self.score1=Score(workout=self.work1, measure=self.meas1, result=2201)
		self.score1.save()
		self.score2=Score(workout=self.work1, measure=self.meas2, result=3220)
		self.score2.save()

	def test_home_page_exists_and_uses_correct_template(self):
		response = self.client.get(reverse('getfit.views.home'))
		template_names_used = [t.name for t in response.templates]
		self.assertIn('home.html', template_names_used)
		
	def test_home_page_displays_exercises_and_dates(self):
		response = self.client.get(reverse('getfit.views.home'))
		self.assertIn(self.work1.exercise.name, response.content)
		self.assertIn(self.work2.exercise.name, response.content)
		self.assertIn(self.work1.time_of_workout.astimezone(self.eastern).strftime("%A %d %B %Y"), response.content)
		self.assertIn(self.work2.time_of_workout.astimezone(self.eastern).strftime("%A %d %B %Y"), response.content)
		
	def test_workout_page_exists_and_uses_correct_template(self):
		response = self.client.get(reverse('getfit.views.workout', args=[self.work2.id,]))
		template_names_used = [t.name for t in response.templates]
		self.assertIn('workout.html', template_names_used)
		
	def test_home_page_links_to_workout_pages(self):
		response = self.client.get(reverse('getfit.views.home'))
		work1_url = reverse('getfit.views.workout', args=[self.work1.id,])
		self.assertIn(work1_url, response.content)
		work2_url = reverse('getfit.views.workout', args=[self.work2.id,])
		self.assertIn(work2_url, response.content)
		
	def test_workout_page_lists_exercise_and_date_and_time_of_workout(self):
		response = self.client.get(reverse('getfit.views.workout', args=[self.work2.id,]))
		self.assertIn(self.work2.exercise.name, response.content)
		self.assertIn(self.work2.time_of_workout.astimezone(self.eastern).strftime("%A %d %B %Y"), response.content)
		self.assertIn(self.work2.time_of_workout.astimezone(self.eastern).strftime("%H:%M"), response.content)
		
	def test_workout_lists_each_score(self):
		response = self.client.get(reverse('getfit.views.workout', args=[self.work1.id,]))
		self.assertIn(self.meas1.name, response.content)
		self.assertIn(self.score2.measure.name, response.content)
		self.assertIn(str(self.score1.result), response.content)
		self.assertIn(u"3220", response.content)
		
	def test_workout_page_has_a_form(self):
		form = WorkoutScoreForm(self.work1)
		self.assertEqual(form.fields.keys(), [self.score1.measure.name, self.score2.measure.name])
		self.assertEqual([form.fields[c].initial for c in form.fields], [2201, 3220])
		response = self.client.get(reverse('getfit.views.workout', args=[self.work1.id,]))		
		self.assertTrue(isinstance(response.context['form'], WorkoutScoreForm))
		
	def test_workout_can_handle_a_change_via_POST(self):
		post_data = {'Reps': str(22022), 'Time': str(4331)}
		response=self.client.post(reverse('getfit.views.workout', args=[self.work1.id,]), data=post_data)

		changedWorkout = Workout.objects.get(pk=self.work1.id)
		self.assertEquals(changedWorkout.score_set.all()[0].result, 22022)
		self.assertEquals(changedWorkout.score_set.all()[1].result, 4331)
		self.assertRedirects(response, reverse('getfit.views.home'))
		
	def test_homepage_has_a_link_to_add_new_workout(self):
		response = self.client.get(reverse('getfit.views.home'))
		self.assertIn(reverse('getfit.views.add'), response.content)
		
	def test_add_page_exists_and_uses_correct_template(self):
		response = self.client.get(reverse('getfit.views.add'))
		template_names_used = [t.name for t in response.templates]
		self.assertIn('add.html', template_names_used)

	def test_add_page_has_a_form(self):
		form = NewWorkoutForm()
		self.assertEqual(form.fields.keys(), ["exercise","time_of_workout"])
		self.assertEqual(form.fields["exercise"].initial, None)
		response = self.client.get(reverse('getfit.views.add'))		
		self.assertTrue(isinstance(response.context['form'], NewWorkoutForm))
		
	def test_add_view_can_create_a_new_workout(self):
		post_data = {'exercise': str(self.exer1.id), 'time_of_workout': "2010-05-01 15:15"}
		response = self.client.post(reverse('getfit.views.add'), data=post_data)
		self.assertEquals(len(Workout.objects.all()), 3)
		self.assertRedirects(response, reverse('getfit.views.workout', args=[3,]))

		post_data = {'exercise': str(self.exer2.id), 'time_of_workout': "2010-05-01 16:16"}
		response = self.client.post(reverse('getfit.views.add'), data=post_data)
		self.assertEquals(len(Workout.objects.all()), 4)

		response = self.client.get(reverse('getfit.views.workout', args=[3,]))		
		self.assertIn("Reps", response.content)
		self.assertIn("Time", response.content)
		
		response = self.client.get(reverse('getfit.views.workout', args=[4,]))		
		self.assertNotIn("Reps", response.content)
		self.assertIn("Time", response.content)
		
	def test_add_view_cant_create_workout_with_invalid_date(self):
		post_data = {'exercise': str(self.exer1.id), 'time_of_workout': "2010-565-01 15:15"}
		response = self.client.post(reverse('getfit.views.add'), data=post_data)
		self.assertEquals(len(Workout.objects.all()), 2)
		self.assertIn('Enter a valid date/time', response.content)

	def test_add_view_cant_create_workout_with_invalid_exercise(self):
		post_data = {'exercise': "700", 'time_of_workout': "2010-05-01 15:15"}
		response = self.client.post(reverse('getfit.views.add'), data=post_data)
		self.assertEquals(len(Workout.objects.all()), 2)
		self.assertIn('Select a valid choice', response.content)
		
	def test_workout_view_has_delete_button(self):
		response = self.client.get(reverse('getfit.views.workout', args=[self.work1.id,]))
		self.assertIn("Delete this workout", response.content)

	def test_deleting_a_workout_removes_it(self):
		response = self.client.get(reverse('getfit.views.delete', args=[self.work1.id,]))
		self.assertEquals(len(Workout.objects.all()), 1)
		self.assertRedirects(response, reverse('getfit.views.home'))
		
	def test_trying_to_open_an_invalid_workout_tells_you_it_doesnt_exist(self):
		response = self.client.get('/workout/200/')
		self.assertIn("That workout doesn't exist", response.content)

	def test_trying_to_delete_an_invalid_workout_tells_you_it_doesnt_exist(self):
		response = self.client.get(reverse('getfit.views.workout', args=[200,]))
		self.assertIn("That workout doesn't exist", response.content)
		
	def test_workout_view_has_edit_button(self):
		response = self.client.get(reverse('getfit.views.workout', args=[self.work1.id,]))
		self.assertIn("Edit this workout", response.content)

	def test_editing_a_workout_date_updates_it(self):
		post_data = {'exercise': str(self.exer1.id), 'time_of_workout': "2010-06-01 15:15"}
		response = self.client.post(reverse('getfit.views.edit', args=[self.work1.id,]), data=post_data)
		self.assertEquals(len(Workout.objects.all()), 2)
		self.assertRedirects(response, reverse('getfit.views.workout', args=[self.work1.id,]))
		chgdWorkout = Workout.objects.get(pk = self.work1.id)
		self.assertEquals("Tuesday 01 June 2010", chgdWorkout.time_of_workout.astimezone(self.eastern).strftime("%A %d %B %Y"))

	def test_editing_a_workout_exercise_updates_it(self):
		self.assertEquals(self.work1.exercise, self.exer1)
		post_data = {'exercise': str(self.exer2.id), 'time_of_workout': str(self.work1.time_of_workout.astimezone(self.eastern).strftime('%Y-%m-%d %H:%M'))}
		response = self.client.post(reverse('getfit.views.edit', args=[self.work1.id,]), data=post_data)
		self.assertEquals(len(Workout.objects.all()), 2)
		self.assertRedirects(response, reverse('getfit.views.workout', args=[self.work1.id,]))
		chgdWorkout = Workout.objects.get(pk = self.work1.id)
		self.assertEquals(chgdWorkout.exercise, self.exer2)
	
	def test_home_page_has_a_link_back_to_itself(self):
		response = self.client.get(reverse('getfit.views.home'))
		self.assertIn('href= "' + reverse('getfit.views.home') + '"', response.content)

	def test_add_page_has_a_link_to_homepage(self):
		response = self.client.get(reverse('getfit.views.add'))
		self.assertIn('href= "' + reverse('getfit.views.home')  + '"', response.content)

	def test_add_page_has_a_link_to_homepage(self):
		response = self.client.get(reverse('getfit.views.add'))
		self.assertIn(reverse('getfit.views.add'), response.content)

