
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import urllib2
import time
from selenium.webdriver.support.ui import Select
import string

from selenium.webdriver.common.keys import Keys
from colorama import Fore, Back, Style
import lxml.html
from StringIO import StringIO

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



f = open('photos_likes_list.txt')
lines = f.readlines()
a = lines[0].split(',')
print type(lines[0])

b = []
for i in a:

	i = i.replace('[','')
	i = i.replace(']','')
	i = i.replace("u'",'')
	i = i.replace("'",'')
	i = i.strip()
	# i = i.replace(i[0],'')

	b.append(i)
	# print type(i)
	# print i + '@@@@@@@@@'
# print b
print "#################"


def fb_login(email,passw):
	
	url = "https://www.facebook.com/"
	browser.get(url)
	email_blank = browser.find_element_by_id("email")
	password = browser.find_element_by_id("pass")
	# submitbtn = browser.find_element_by_id('u_0_n')
	email_blank.send_keys(email)
	password.send_keys(passw)
	# submitbtn.click()
	password.send_keys(Keys.RETURN)

	print "LOGGED IN" + Fore.YELLOW + "\n"


def get_people(photos_likes_list):

	All_names = []
	All_names_list=[]
	for item in photos_likes_list:
		print Fore.GREEN+ "IN photos_likes_list"  + "\n"
		url = "https://www.facebook.com%s" % (item)
		print url + Fore.YELLOW + "\n"
		browser.get(url)
		time.sleep(1)

	
		i = 0;
		try:
			while (True):
				print i
				i = i+1

				a = browser.find_element_by_css_selector('.pam.uiBoxLightblue.uiMorePagerPrimary').click()
				wait = WebDriverWait(browser, 5);
				##the browser will wait until the button "see more" is available and if its no more available 
				## an err is thrown the loop is broken
				elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pam.uiBoxLightblue.uiMorePagerPrimary')));
				print elem
				# print len(a)

		except Exception as e:

			print e 

			pass

		print "###############################################"
		print browser
		html_source = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
		people_list_soup = BeautifulSoup(html_source  , 'html.parser')


		a=people_list_soup .find_all("div", class_="_5j0e fsl fwb fcb")

		count = 0
		for item in a:
			count = count+1
			name = item.text.strip()
			if  name not in All_names_list:
				All_names_list.append(name)
				All_names.append((name,item.a['href']))
			else :
				print name
	return All_names

username = ''
password = ''
browser = webdriver.Firefox()
fb_login(username,password)
time.sleep(5)
names = get_people(b)

print >> open('test.txt','w'), names

browser.close()
exit()
