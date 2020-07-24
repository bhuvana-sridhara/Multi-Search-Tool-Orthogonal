from selenium import webdriver
import webbrowser
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import sys

import config as cfg

class confluence_scrape(object):

	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--incognito')
		options.add_argument('--headless')
		self.driver = webdriver.Chrome("/Users/bhuvanasridhara/Downloads/chromedriver", chrome_options=options)

		self.driver.get("https://orthogonal.atlassian.net/wiki/home")

		self.email = input("Login email: ")
		if(not "@" in self.email):
			print ("Please include an \"@\" in the email address")
			sys.exit(1)
		# TODO more negative cases handling.

		self.password = input("Password: ")

	def search(self,search_term):
		#find username
		# self.driver.find_element_by_id("username").send_keys(cfg.login["email"])
		self.driver.find_element_by_id("username").send_keys(self.email)

		# find continue
		button = self.driver.find_element_by_class_name("css-1eyj9fn")
		ActionChains(self.driver).move_to_element(button).click(button).perform()

		wait = WebDriverWait(self.driver, 10)
		try:
			men_menu = wait.until(ec.visibility_of_element_located((By.ID, "password")))
		except TimeoutException:
			print ("Wrong login email!")
			sys.exit(1)
		#find password
		# self.driver.find_element_by_id("password").send_keys(cfg.login["password"])
		self.driver.find_element_by_id("password").send_keys(self.password)
		button = self.driver.find_element_by_class_name("css-1eyj9fn")
		ActionChains(self.driver).move_to_element(button).click(button).perform()

		#wait until page loads
		try:
			men_menu = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "css-15i33f0")))
		except TimeoutException:
			print ("Confluence took too long to load! Check login email and password and try again")
			sys.exit(1)
		#find search button
		search_button = self.driver.find_element_by_xpath('//*[@id="confluence-ui"]/div[3]/div/div[1]/div/header/div/div/div/div/div/div/div/span')
		ActionChains(self.driver).move_to_element(search_button).click(search_button).perform()

		search_bar = self.driver.find_element_by_xpath('//*[@id="confluence-ui"]/div[3]/div/div[1]/div/header/div/div/div/div/div/div[1]/div/input')
		search_bar.send_keys(search_term)
		search_bar.send_keys(Keys.RETURN)

		wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="content-body"]/div/div/div[1]/form/div/div[2]/button/span/span/span')))
		search_button = self.driver.find_element_by_xpath('//*[@id="content-body"]/div/div/div[1]/form/div/div[2]/button/span/span/span')
		ActionChains(self.driver).move_to_element(search_button).click(search_button).perform()

		self.driver.implicitly_wait(10)

		page_source = self.driver.page_source
		soup = BeautifulSoup(page_source, 'lxml')

		search_output = soup.find_all('div', class_='sc-iuDHTM kAsuib')

		f = open("search results.html", "a")
		f.write('<br><br>'+"Files found in Confluence:"+ '\n')
		for search_selector in search_output:			
			clickable_link = "https://orthogonal.atlassian.net"+search_selector.a.get("href")
			f.write('<li>' + '<a href=\"' + clickable_link + '\"</a>'+'</li>' )
			f.write (search_selector.a.text)
			# make_list = '<li>{}</li>'.format("https://orthogonal.atlassian.net"+search_selector.a)
			# make_list = '<li>{}</li>'.format(clickable_link)
			# make_list = '<li>{}</li>'.format(search_selector.a)
			
			# f.write('{}\n'.format(make_list))
			# f.write (search_selector.a.text+": ")
			# f.write ("https://orthogonal.atlassian.net"+search_selector.a.get("href") + "\n \n")

		f.close()

		# self.driver.get_screenshot_as_file("screenshot.png")