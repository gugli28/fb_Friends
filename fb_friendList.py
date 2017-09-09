#!/usr/bin/env python
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

import argparse

SCROLL_PAUSE_TIME = 4
def speed_Scroll():
	

	# Get scroll height
	last_height = browser.execute_script("return document.body.scrollHeight")
	i =0;
	# while (i<1000):
	# 	i = i +1
	# 	print i
	while True:
		# Scroll down to bottom
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = browser.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			print "SCROLLED" + Fore.YELLOW + "\n"
			break
		last_height = new_height

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


def get_all_photos(target):
	url = "https://www.facebook.com/%s/photos?" % (target)
	# scroll till the lazy loading finishes
	

	#Get page source
	browser.get(url)
	time.sleep(1)
	speed_Scroll()
	html_source = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

	# html_source = browser.page_source
	photos_soup = BeautifulSoup(html_source  , 'html.parser')
	# print(soup.prettify())


	# photos_list = photos_soup.find_all("a")
	
	photos_list = photos_soup.find_all("a", class_="uiMediaThumb _6i9 uiMediaThumbMedium")

	####printing the photos list in a file

	all_pics = []
	for item in photos_list:
		all_pics.append(item['href'])

	return all_pics
	# print >>open('photos_list1.txt','w'),photos_list

	# print photos_list
	# print photos_soup

def get_photos_likes_list(all_pics):
	# url = "https://www.facebook.com/photo.php?fbid=1318691198258466&set=pb.100003527947880.-2207520000.1503535383.&type=3&theater"
	print "GET PHOTOS LIKES" + Fore.BLUE + "\n"

	# print all_pics
	photos_likes_link_list = []
	photo_no = 1
	for item in all_pics:
		url = item
		try:
			browser.get(url)
		except Exception as e:
			continue
		time.sleep(1)
		
		html_source = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

		# html_source = browser.page_source
		photos_likes_soup = BeautifulSoup(html_source  , 'html.parser')

		photos_likes_link = photos_likes_soup.find("a", class_="_2x4v")

		
		###couldnt retrieve link at some place
		photo_no +=1
		try:
			photos_likes_link_list.append(photos_likes_link['href'])
		except Exception as e:
			print "GOT err in finding list of likes of photo no %s" %(photo_no) + Fore.RED + "\n"
			pass
		

	return photos_likes_link_list
	# print photos_likes_list

	# print photos_likes_link

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
#=============================================================================================================
#INPUT
print "EXAMPLE FOR PASSING THE ARGUMENTS"
print "python fb_frnd_list.py -username blahblah@blah.com -password blahblahbl -target_prof zuck -output report.txt"

parser = argparse.ArgumentParser(usage="-h for full usage")

parser.add_argument('-username', dest="username", help='facebook username to login with (e.g. example@example.com)',required=True)
parser.add_argument('-password', dest="password", help='facebook password to login with (e.g. \'password\')',required=True)
parser.add_argument('-target_prof', dest="target_prof", help='(e.g. "text.example")',required=False)
parser.add_argument('-output', dest="output", help='File name to save results',required=False)

args = parser.parse_args()

######
print args
print parser


target = args.target_prof
username = args.username
password = args.password
filename = args.output

browser = webdriver.Firefox()

fb_login(username,password)
time.sleep(5) 
# speed_Scroll()
all_pics = get_all_photos(target)
print >>open('photos_list.txt','w'),all_pics
print "PRINTED PHOTOS LIST in photos_list.txt. Save it if u want, in another file, FILES GONNA BE REWRITTEN"

photos_likes_list = get_photos_likes_list(all_pics)
print >>open('photos_likes_list.txt','w'),photos_likes_list
print "PRINTED PHOTOS LIST in photos_likes_list.txt. Save it if u want, in another file, FILES GONNA BE REWRITTEN"

All_names = get_people(photos_likes_list)

count = 1
file_name = open(filename,'w');
for item in All_names:
	print item
	print >> file_name , item[0].encode('utf-8')
	print >> file_name , item[1].encode('utf-8')
	print >> file_name , "#####################################"
	
	count = count +1

print >> file_name , len(all_pics ) 
print >> file_name , "TOtal FRIENDS COUNT = ",len(All_names)
print len(all_pics ),len(photos_likes_list )
print  "TOtal FRIENDS COUNT = ",len(All_names)

browser.close()
exit()

