from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import login

class ExerciseTest(LiveServerTestCase):
	fixtures = ['adminUser.json']
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
		
	def test_can_setup_some_workouts_via_admin(self):
		self._setup_workouts_via_admin()

		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Site administration', body.text)

		self.assertFail("todo")
		
	def _setup_workouts_via_admin(self):
		self.browser.get(self.live_server_url + '/admin/')
				
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys(login.un)

		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys(login.pw)
		password_field.send_keys(Keys.RETURN)
		
