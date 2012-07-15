from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import login

class ExerciseTest(LiveServerTestCase):
	fixtures = ['adminUser.json']
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		self._setup_workouts_via_admin()
		
	def tearDown(self):
		self.browser.quit()
		pass
		
	def _setup_workouts_via_admin(self):
		self.browser.get(self.live_server_url + '/admin/')
				
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys(login.un)

		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys(login.pw)
		password_field.send_keys(Keys.RETURN)

		self.browser.find_element_by_link_text('Measures').click()
		self.browser.find_element_by_link_text('Add measure').click()

		name_field = self.browser.find_element_by_name('name')
		name_field.send_keys('Length')
		
		save_button = self.browser.find_element_by_name("_addanother")
		save_button.click()

		name_field = self.browser.find_element_by_name('name')
		name_field.send_keys('Width')
		
		save_button = self.browser.find_element_by_name("_save")
		save_button.click()

		self.browser.find_element_by_link_text('Getfit').click()
		self.browser.find_element_by_link_text('Exercises').click()
		self.browser.find_element_by_link_text('Add exercise').click()
			
		name_field = self.browser.find_element_by_name('name')
		name_field.send_keys('Jumping')
		self.browser.find_elements_by_tag_name("option")[0].click()
		
		save_button = self.browser.find_element_by_name("_addanother")
		save_button.click()
		
		name_field = self.browser.find_element_by_name('name')
		name_field.send_keys('Reaching')
		self.browser.find_elements_by_tag_name("option")[1].click()

		save_button = self.browser.find_element_by_name("_save")
		save_button.click()

		self.browser.find_element_by_link_text('Getfit').click()
		self.browser.find_element_by_link_text('Workouts').click()
		self.browser.find_element_by_link_text('Add workout').click()

		self.browser.find_element_by_xpath("//select[@name='exercise']/option[@value='1']").click()
		self.browser.find_element_by_link_text('Today').click()
		self.browser.find_element_by_link_text('Now').click()
		self.browser.find_element_by_xpath("//select[@name='score_set-0-measure']/option[@value='1']").click()
		result = self.browser.find_element_by_xpath("//input[@name='score_set-0-result']")
		result.send_keys('12345')

		save_button = self.browser.find_element_by_name("_addanother")
		save_button.click()
		
		self.browser.find_element_by_xpath("//select[@name='exercise']/option[@value='2']").click()
		self.browser.find_element_by_link_text('Today').click()
		self.browser.find_element_by_link_text('Now').click()
		self.browser.find_element_by_xpath("//select[@name='score_set-0-measure']/option[@value='2']").click()
		result = self.browser.find_element_by_xpath("//input[@name='score_set-0-result']")
		result.send_keys('67890')
		
		save_button = self.browser.find_element_by_name("_save")
		save_button.click()
	
		self.browser.find_element_by_link_text('Log out').click()
		
	def test_flow_through_the_site(self):
		
		#Visit main page
		self.browser.get(self.live_server_url)

		body = self.browser.find_element_by_tag_name('body')

		#Check all the admin setup stuff is shown
		self.assertIn('Workouts', body.text)
		self.assertIn('Jumping', body.text)
		self.assertIn('Reaching', body.text)

		#Visit the link for the first admin setup exercise
		self.browser.find_element_by_link_text('Jumping').click()

		body = self.browser.find_element_by_tag_name('body')

		#and confirm details are correct
		self.assertIn('Jumping', body.text)
		self.assertIn('Length', body.text)
		self.assertIn('12345', self.browser.page_source)

		self.browser.get(self.live_server_url)

		#now visit the second 
		self.browser.find_element_by_link_text('Reaching').click()

		body = self.browser.find_element_by_tag_name('body')

		#and check everything is there
		self.assertIn('Reaching', body.text)
		self.assertIn('Width', body.text)
		self.assertIn('67890', self.browser.page_source)

		#now check we can navigate to a workout directly
		self.browser.get(self.live_server_url + '/workout/1/')

		body = self.browser.find_element_by_tag_name('body')

		#and that all the details are still correct
		self.assertIn('Jumping', body.text)
		self.assertIn('Length', body.text)
		self.assertIn('12345', self.browser.page_source)

		#now check we can update the result for one of the measures
		result_field = self.browser.find_element_by_name('Length')
		result_field.clear()
		result_field.send_keys('345678')
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()

		#and that if we revisit the page the change stuck
		self.browser.get(self.live_server_url + '/workout/1/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Jumping', body.text)
		self.assertIn('Length', body.text)
		self.assertIn('345678', self.browser.page_source)
	
		#then go back to homepage
		self.browser.find_element_by_link_text("Home").click()

		#and follow the add link to create a new workout
		self.browser.find_element_by_link_text("Add").click()

		#choose the second type of exercise
		self.browser.find_element_by_xpath("//select/option[@value='2']").click()
		self.browser.find_element_by_link_text("Today").click()
		self.browser.find_element_by_link_text("Now").click()
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()

		#we should have been taken to the result editing page and be presented with appropriate choices
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Reaching', body.text)
		self.assertIn('Width', body.text)

		#find the result field and set the result
		result_field = self.browser.find_element_by_name('Width')
		result_field.clear()
		result_field.send_keys('234')
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()
		
		#check it looks like we are back on the homepage
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Workouts', body.text)
		self.assertIn('Jumping', body.text)
		self.assertIn('Reaching', body.text)
		
		#Now try to follow the link to our new workout
		self.browser.find_element_by_link_text("Reaching").click()
		
		#and check the new result was logged
		self.assertIn('234', self.browser.page_source)
		
		#now try to add a new workout directly
		self.browser.get(self.live_server_url + '/workout/add/')

		#give an invalid date
		date_field = self.browser.find_element_by_name('time_of_workout_0')
		date_field.clear()
		date_field.send_keys('2010-565-23')
		time_field = self.browser.find_element_by_name('time_of_workout_1')
		time_field.clear()
		time_field.send_keys('15:15')
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()
		
		#Check we were told off for entering an invalid choice
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Enter a valid date', body.text)
		
		#Now go back to the first workout
		self.browser.get(self.live_server_url + '/workout/1/')

		#And try to alter the score to an invalid one
		result_field = self.browser.find_element_by_name('Length')
		result_field.clear()
		result_field.send_keys('34ss5678')
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()

		#Check we were told off for entering an invalid choice
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Enter a number', body.text)

		#Now go back to the first workout
		self.browser.get(self.live_server_url + '/workout/1/')
		
		#And try to delete it
		self.browser.find_element_by_link_text("Delete this workout").click()
		
		#Now try to reopen the workout
		self.browser.get(self.live_server_url + '/workout/1/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn("That workout doesn't exist", body.text)
		
		#Now try to directly delete a non-existent workout
		self.browser.get(self.live_server_url + '/workout/1/delete')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn("That workout doesn't exist", body.text)

		#Now go to the second workouts edit view
		self.browser.get(self.live_server_url + '/workout/2/edit/')
		
		#And try to edit it
		date_field = self.browser.find_element_by_name('time_of_workout_0')
		date_field.clear()
		date_field.send_keys('2010-06-24')
		time_field = self.browser.find_element_by_name('time_of_workout_1')
		time_field.clear()
		time_field.send_keys('15:15')
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()
		
		#Now try to reopen the workout and check the date changed
		self.browser.get(self.live_server_url + '/workout/2/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn("Thursday 24 June 2010 @ 15:15", body.text)
		self.assertIn("Reaching", body.text)
		
		#Now go to the second workout 
		self.browser.get(self.live_server_url + '/workout/2/')
		
		#And try to edit it
		self.browser.find_element_by_link_text("Edit this workout").click()
		self.browser.find_element_by_xpath("//select/option[@value='1']").click()
		date_field = self.browser.find_element_by_name('time_of_workout_0')
		date_field.clear()
		date_field.send_keys('2010-06-23')
		time_field = self.browser.find_element_by_name('time_of_workout_1')
		time_field.clear()
		time_field.send_keys('15:15')
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()
		
		#Now try to reopen the workout and check the date changed
		self.browser.get(self.live_server_url + '/workout/2/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn("Wednesday 23 June 2010 @ 15:15", body.text)
		self.assertIn("Jumping", body.text)
		
		#Now try to follow the Measures Link
		self.browser.find_element_by_link_text("Measures").click()

		#Check the page shows our existing measures
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn("Length", body.text)
		self.assertIn("Width", body.text)

		#Check the page doesn't have a delete facility
		self.assertNotIn("Delete", body.text)
		
		#Check it does have an add button/link
		self.assertIn("Add measure", body.text)
		
		#follow the link to add a new measure
		self.browser.find_element_by_link_text("Add measure").click()
		
		#Try to add a new measure
		measure_field = self.browser.find_element_by_name('name')
		measure_field.send_keys('Breadth')
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()
		
		#Now Navigate back to the measures page and verify that the measure is there
		self.browser.get(self.live_server_url + '/measures/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn("Breadth", body.text)
		
		#Now try to visit the Exerices Link
		self.browser.find_element_by_link_text("Exercises").click()
		
		#Check the page shows our existing exercises
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn("Jumping", body.text)
		self.assertIn("Reaching", body.text)
		
		#Check the page doesn't have a delete facility
		self.assertNotIn("Delete", body.text)
		
		#Check it does have an add button/link
		self.assertIn("Add exercise", body.text)
		
		#follow the link to add a new exercise
		self.browser.find_element_by_link_text("Add exercise").click()
		
		#Try to add a new exercise
		exercise_field = self.browser.find_element_by_name('name')
		exercise_field.send_keys('Stretching')
		self.browser.find_element_by_xpath("//input[@value='2']").click()
		self.browser.find_element_by_xpath("//input[@value='3']").click()
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()
		
		#Now Navigate back to the measures page and verify that the measure is there
		self.browser.get(self.live_server_url + '/exercises/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Stretching', body.text)
		
		#Now let's add a new workout with our new exercise and measure
		self.browser.find_element_by_link_text("Add").click()
		self.browser.find_element_by_xpath("//select/option[@value='3']").click()
		self.browser.find_element_by_link_text("Today").click()
		self.browser.find_element_by_link_text("Now").click()
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()

		#we should have been taken to the result editing page and be presented with appropriate choices
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Stretching', body.text)
		self.assertIn('Breadth', body.text)
		self.assertIn('Width', body.text)
		self.assertNotIn('Length', body.text)

		#find the result field and set the result
		result_field = self.browser.find_element_by_name('Width')
		result_field.clear()
		result_field.send_keys('234')
		result_field = self.browser.find_element_by_name('Breadth')
		result_field.clear()
		result_field.send_keys('345')
		save_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		save_button.click()
		