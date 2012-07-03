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
		
	def test_homepage_includes_workouts_setup_by_admin(self):
		self.browser.get(self.live_server_url)

		body = self.browser.find_element_by_tag_name('body')

		self.assertIn('Workouts', body.text)
		self.assertIn('Jumping', body.text)
		self.assertIn('Reaching', body.text)
		
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
		
	def test_following_links_from_homepage_takes_me_to_workouts(self):
		self.browser.get(self.live_server_url)

		self.browser.find_element_by_link_text('Jumping').click()

		body = self.browser.find_element_by_tag_name('body')

		self.assertIn('Jumping', body.text)
		self.assertIn('Length', body.text)
		self.assertIn('12345', self.browser.page_source)

		self.browser.get(self.live_server_url)

		self.browser.find_element_by_link_text('Reaching').click()

		body = self.browser.find_element_by_tag_name('body')

		self.assertIn('Reaching', body.text)
		self.assertIn('Width', body.text)
		self.assertIn('67890', self.browser.page_source)

