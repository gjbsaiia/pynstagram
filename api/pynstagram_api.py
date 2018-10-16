
import os
import sys
import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date
# my Libraries
from instaDictionaries import xpathDic
from classDefinitions import profile
from classDefinitions import post

# Description: Takes new Profile object and moves login data into structure. Begins clockself.
# Parameters: me - Profile
def unpackMe(me):
	with open(me.login, "r") as file:
		lines = file.readlines()
	file.close()
	user = lines[0].split("Username = ")[1]
	password = lines[1].split("Password = ")[1]
	s = lines[2].split("Size = ")[1]
	if(s == "big" or s == "Big"):
		size = True
	else:
		size = False
	try:
		sheetName = (lines[3].split("Google Sheet Name = ")[1]).split("\n")[0]
		me.sheetName = sheetName
		me.configCreds()
	except IndexError:
		me.sheetName = ""
	me.username = user
	me.password = password
	me.size = size
	me.startTime()

# Description: Initializes webdriver, logins to instagram.
# Parameters: me - profile object
#			  headless - boolean
# Return: Webdriver, or False on failure
def start(me, headless):
	user = me.username
	password = me.password
	options = Options()
	if(headless):
		options.add_argument("--headless")
	options.add_argument("disable-infobars")
	options.add_argument("--disable-extensions")
	driver = webdriver.Chrome(chrome_options=options)
	driver.set_window_size(1120, 750)
	driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic["user"])))
	elm1=driver.find_element_by_xpath(xpathDic["user"])
	elm1.click()
	elm1.send_keys(user)
	elm2=driver.find_element_by_xpath(xpathDic["password"])
	elm2.click()
	elm2.send_keys(password)
	#Click on login
	elm4=driver.find_element_by_xpath(xpathDic["submit"])
	elm4.click()
	time.sleep(2)
	try:
		try:
			element = driver.find_element_by_xpath(xpathDic["notif"])
		except selenium.common.exceptions.NoSuchElementException:
			element = driver.find_element_by_xpath(xpathDic["trickyNotif"])
		element.click()
	except: # when running headless, notifications not offered
		k = 0
	time.sleep(2)
	try:
		element = driver.find_element_by_xpath(xpathDic["profile"])
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic["profile"])))
		elm5=driver.find_element_by_xpath(xpathDic["profile"])
		elm5.click()
	except selenium.common.exceptions.NoSuchElementException:
		logError("In START(): Login Failed. Check if account is flagged or if login information is correct.")
		return False
	except selenium.common.exceptions.TimeoutException:
		logError("In START(): Login Failed. Check if account is flagged or if login information is correct.")
		return False
	return driver

# Description: Utility method that generalizes how lists are preloaded.
# Parameters: driver - webdriver with a currently open list
#			  limit - total possible number of items in list
#			  type - string, ( "like" or "user" )
# Return: No. of list items on successful scroll, False on fail
def loadList(driver, limit, type, size):
	try:
		time.sleep(1)
		if(type == "like" or "user"):
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic[type+"List"])))
			currentList = len(driver.find_elements_by_xpath(xpathDic[type+"List"]))
			element = driver.find_element_by_xpath(xpathDic[type+"Frame"])
			dimensions = element.size
			# finds arrow down button
			x = dimensions["width"] - 3
			y = dimensions["height"] - 3
			followerrs = []
			r = 0
			while(currentList != limit):
				clickAndHold(driver, element, x, y, 5, size)
				if(currentList == len(driver.find_elements_by_xpath(xpathDic[type+"List"]))):
					r += 1
					if(r == 5):
						break
				currentList = len(driver.find_elements_by_xpath(xpathDic[type+"List"]))
			return currentList
	except selenium.common.exceptions.NoSuchElementException:
		logError("In LOADLIST: lost "+type+"List element. Investigate with headless mode disabled, and check if down arrow is getting pressed.\nLOADLIST is used by SCRAPESELF and SCRAPELIKES.")
		return False
	except selenium.common.exceptions.TimeoutException:
		logError("In LOADLIST: Unable to locate "+type+"List element. Check element's xpath, and update your xpathDictionary. Please post issue on git with correct xpath.\nLOADLIST is used by SCRAPESELF and SCRAPELIKES.")
		return False

# Description: Utility method that clicks and holds location on element
# Parameters: driver - running webdriver
#			  element - element to be clicked on
#			  x - location across width
#			  y - location across height
#			  t - time held
#			  size - boolean, True = big, False = small
# ** Note: (x,y) are distanced from top left corner of element **
def clickAndHold(driver, element, x, y, t, size):
	action = webdriver.common.action_chains.ActionChains(driver)
	action.move_to_element_with_offset(element, x, y)
	action.click_and_hold()
	action.perform()
	time.sleep(t)
	action2 = webdriver.common.action_chains.ActionChains(driver)
	action2.move_to_element_with_offset(element, x, y)
	action2.release()
	action2.perform()
	if(size):
		time.sleep(5)

# Description: Utility method that takes strips listitems into list
# Parameters: driver - running webdriver
#			  limit - int, actual list length
#			  type - string, "user"/"liker"/"commenter"
# Return: returns list of items on success, returns False on failure
def scrapeList(driver, limit, type):
	try:
		list = []
		if(type == "commenter"):
			i = 2
		else:
			i = 1
		while i <= limit:
			newxpath = xpathDic[type+"Pt1"]+str(i)+xpathDic[type+"Pt2"]
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, newxpath)))
			element = driver.find_element_by_xpath(newxpath)
			text = str(element.get_attribute("title"))
			user = text
			list.append(user)
			i += 1
		if not(type == "commenter"):
			elm8 = driver.find_element_by_xpath(xpathDic["exit"+type+"List"])
			elm8.click()
		return list
	except selenium.common.exceptions.TimeoutException:
		logError("In SCRAPELIST: unable to find "+type+" list item "+i+". Probably the page stopped loading. Add delay in loop. Add issue on Git. \nSCRAPELIST is used by SCRAPESELF, SCRAPECOMMENTS, SCRAPELIKES.")
		return False

# Description: Populates profile object with follower count, follower list, following count, following list.
#		    	Finds NonFollowBackers, and appends them to shit list.
# Parameters:	me - Profile object
#				driver - running webdriver
def scrapeSelf(me, driver):
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic["followersCount"])))
	text = driver.find_element_by_xpath(xpathDic["followersCount"]).text
	# necessary for 1000+ scalability
	try:
		me.defNumFollowers(text)
	except ValueError:
		split = text.split(",")
		num = split[0]+split[1]
		me.defNumFollowers(num)
	elm6 = driver.find_element_by_xpath(xpathDic["followers"])
	elm6.click()
	limit = loadList(driver, me.numFollowers, "user", me.size)
	followers = scrapeList(driver, limit, "user")
	for each in followers:
		me.addFollower(each)
		me.followerIndex[each] = (0, 0, False, '')
	text = driver.find_element_by_xpath(xpathDic["followingCount"]).text
	try:
		me.defNumFollowing(text)
	except ValueError:
		split = text.split(",")
		num = split[0]+split[1]
		me.defNumFollowing(num)
	element = driver.find_element_by_xpath(xpathDic["following"])
	element.click()
	limit = loadList(driver, me.numFollowing, "user", me.size)
	following = scrapeList(driver, limit, "user")
	for each in following:
		try:
			exists = me.followerIndex[each]
			me.followerIndex[each] = (0, 0, True, '')
			me.addFollowee(each)
		except KeyError:
			me.addFollowee(each)
	me.defaultShitList()

# Description: Appends posts to the "recentPosts" array in your Profile object up to the specified date.
# Parameters:	me - Profile object
#				driver - running webdriver
#				lastDate - string, "MM/DD/YYYY"
def scrapePostsToDate(me, driver, lastDate):
	splitted = lastDate.split("/")
	last = date(int(splitted[2]),int(splitted[0]),int(splitted[1]))
	cpost = scrapeRecentPost(me,driver,True)
	newDate = cpost.date
	while(((newDate - last).days != 0) and (not (cpost == False))):
		me.addPost(cpost)
		time.sleep(2)
		cpost = scrapeLaterPost(me, driver, True)
		newDate = cpost.date
	element = driver.find_element_by_xpath(xpathDic["exitPics"])
	element.click()
	return me

# Description: Appends posts to the "recentPosts" array in your Profile object up to the specified number of posts.
# Parameters:	me - Profile object
#				driver - running webdriver
#				n - int, number of posts
#				full - boolean, whether or not you want all data from posts
def scrapeNumberOfPosts(me, driver, n, full):
	if(n > 0):
		cpost = scrapeRecentPost(me,driver,full)
	while((not(n == 0)) and (not(cpost == False))):
		me.addPost(cpost)
		time.sleep(2)
		scrapeLaterPost(me, driver, full)
		n -= 1
	element = driver.find_element_by_xpath(xpathDic["exitPics"])
	element.click()
	return me

# Description: Creates and populates post object with specified amount of data for most recent post.
# Parameters:	me - Profile object
#				driver - running webdriver
#				full - boolean, partial or full scrape
# Return: returns profile object on success, returns False on failure
def scrapeRecentPost(me, driver, full):
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic["pic1"])))
	element = driver.find_element_by_xpath(xpathDic["pic1"])
	element.click()
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic["picFrame"])))
	if(full):
		cpost = completelyScrapePost(me, driver)
	else:
		cpost = partialScrapePost(me, driver)
	time.sleep(.5)
	try:
		element = driver.find_element_by_xpath(xpathDic["next"])
	except selenium.common.exceptions.NoSuchElementException:
		logError("In SCRAPERECENTPOST: unable to find next element. Check element's xpath, and update your xpathDictionary. Please post issue on git with correct xpath.")
		return cpost()
	element.click()
	return cpost

# Description: Creates and populates post object with specified amount of data for post other than the first post
# Parameters:	me - Profile object
#				driver - running webdriver
#				full - boolean, partial or full scrape
# Return: returns profile object on success, returns False on failure
def scrapeLaterPost(me, driver, full):
	if(full):
		cpost = completelyScrapePost(me, driver)
	else:
		cpost = partialScrapePost(me, driver)
	time.sleep(.5)
	try:
		element = driver.find_element_by_xpath(xpathDic["nextt"])
	except selenium.common.exceptions.NoSuchElementException:
		logError("In SCRAPELATERPOST: unable to find nextt element. This method must be called after scrapeRecentPost Check element's xpath, and update your xpathDictionary. Please post issue on git with correct xpath.")
		return cpost
	element.click()
	return cpost

# Description: Utility funtion. Creates post object and strips all data from post into it.
#			** Note: must be called with "scrapeRecentPost" or "scrapeLaterPost" **
# Parameters:	me - Profile object
#				driver - running webdriver
# Return: returns post object on success, False on failure
def completelyScrapePost(me, driver):
	cpost = post(me)
	try:
		element = driver.find_element_by_xpath(xpathDic["time"])
	except selenium.common.exceptions.NoSuchElementException:
		try:
			element = driver.find_element_by_xpath(xpathDic["trickyTime"])
		except selenium.common.exceptions.NoSuchElementException:
			logError("In COMPLETELYSCRAPEPOST: unable to find time attribute. Check element's xpath, and update your xpathDictionary. Please post issue on git with correct xpath.")
	cpost.defTime(element.get_attribute("title"))
	try:
		element = driver.find_element_by_xpath(xpathDic["caption"])
		cpost.defCaption(element.text)
	except selenium.common.exceptions.NoSuchElementException:
		cpost.defCaption("")
	scrapeComments(driver, cpost)
	scrapeLikes(driver, cpost)
	return cpost

# Description: Utility funtion. Creates post object and strips basic data from post into it.
#			** Note: must be called with "scrapeRecentPost" or "scrapeLaterPost" **
# Parameters:	me - Profile object
#				driver - running webdriver
# Return: returns post object on success, False on failure
def partialScrapePost(me, driver):
	cpost = post(me)
	comments = loadComments(driver)
	numLikes = getLikes(driver)
	cpost.defNumComments(comments)
	cpost.defNumLikes(numLikes)
	return cpost

# Description: Utility funtion. Loads comment list.
#			** Note: should not be called on its own **
# Parameters: driver - running webdriver
# Return: returns number of comments
def loadComments(driver):
	while True:
		try:
			element = driver.find_element_by_xpath(xpathDic["loadMore"])
		except selenium.common.exceptions.NoSuchElementException:
			try:
				element = driver.find_element_by_xpath(xpathDic["noCaptionLoadMore"])
			except selenium.common.exceptions.NoSuchElementException:
				break
	comments = len(driver.find_elements_by_xpath(xpathDic["commenterList"]))
	return (comments)

# Description: Utility funtion. Scrapes commenters and loads them into post object
#			** Note: should not be called on its own **
# Parameters: driver - running webdriver
#			  cpost - post object
def scrapeComments(driver, cpost):
	comments = loadComments(driver)
	cpost.defNumComments(comments - 1)
	commenters = scrapeList(driver, comments, "commenter")
	for commenter in commenters:
		cpost.addCommenter(commenter)
		try:
			test = cpost.parent.followerIndex[commenter]
			cpost.parent.followerIndex[commenter] = (cpost.parent.followerIndex[commenter][0], cpost.parent.followerIndex[commenter][1]+1, cpost.parent.followerIndex[commenter][2], cpost.parent.followerIndex[commenter][3])
		except KeyError:
			t = 0

# Description: Utility funtion. Retreives number of likes.
#			** Note: should not be called on its own **
# Parameters: driver - running webdriver
# Return: returns number of likes
def getLikes(driver):
	try:
		element = driver.find_element_by_xpath(xpathDic["numLikes"])
	except selenium.common.exceptions.NoSuchElementException:
		logError("In SCRAPELIKES: unable to find number of likes element. Check element's xpath, and update your xpathDictionary. Please post issue on git with correct xpath.")
	try:
		numLikes = int(element.text)
	except ValueError:
		split = element.text.split(",")
		num = split[0]+split[1]
		numLikes = int(num)
	return numLikes

# Description: Utility funtion. Scrapes likers and loads them into post object
#			** Note: should not be called on its own **
# Parameters: driver - running webdriver
#			  cpost - post object
def scrapeLikes(driver, cpost):
	numLikes = getLikes(driver)
	cpost.defNumLikes(numLikes)
	try:
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic["likes"])))
	except selenium.common.exceptions.TimeoutException:
		logError("In SCRAPELIKES: Unable to locate likes element. Check element's xpath, and update your xpathDictionary. Please post issue on git with correct xpath.")
	element = driver.find_element_by_xpath(xpathDic["likes"])
	element.click()
	limit = loadList(driver, cpost.numLikes, "liker", cpost.parent.size)
	likers = scrapeList(driver, limit, "liker")
	for liker in likers:
		cpost.addLiker(liker)
		try:
			test = cpost.parent.followerIndex[liker]
			cpost.parent.followerIndex[liker] = (cpost.parent.followerIndex[liker][0]+1, cpost.parent.followerIndex[liker][1], cpost.parent.followerIndex[liker][2], cpost.parent.followerIndex[liker][3])
		except KeyError:
			t = 0

# Description: Defines top 10 followers. Can only be run after scraping self and some posts.
# Parameters: me - profile object
def getTop10(me):
	rankDic={}
	for key, value in me.followerIndex.items():
		rankDic[key]=(value[0]+(1.1*value[1]))
	rankedFollowing = sorted(rankDic, key=rankDic.get, reverse=True)
	just10 = []
	i = 0
	while(i < 10):
		me.addTop(rankedFollowing[i])
		i += 1

# Description: Finds users with no activity on your profile. Adds them to unfollow list. Can only be run after scraping self and some posts.
# Parameters: me - profile object
def addGhostsToShitList(me):
	rankDic={}
	for key, value in me.followerIndex.items():
		rankDic[key]=(value[0]+(1.1*value[1]))
	ghosts = [key for key,value in rankDic.items() if value == 0]
	me.addToShitList(ghosts)

# Description: Unfollows all users defined in shitlist of your profile object. Can only be run after scrapself.
# Parameters: me - profile object
#			  driver - running webdriver
def unfollow(me, driver):
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic["followingCount"])))
	followingCount = int(driver.find_element_by_xpath(xpathDic["followingCount"]).text)
	element = driver.find_element_by_xpath(xpathDic["following"])
	element.click()
	time.sleep(2)
	limit = loadList(driver, me.numFollowing, "user", me.size())
	i = 1
	while i <= currentList:
		newxpath= xpathDic["userPt1"]+str(i)+xpathDic["userPt2"]
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, newxpath)))
		element = driver.find_element_by_xpath(newxpath)
		text = str(element.get_attribute("title"))
		followee = text
		if followee in me.shitList:
			newxpath= xpathDic["userPt1"]+str(i)+xpathDic["userUnfollow"]
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, newxpath)))
			element = driver.find_element_by_xpath(newxpath)
			element.click()
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic["unfollow"])))
			element = driver.find_element_by_xpath(xpathDic["unfollow"])
			element.click()
			try:
				me.followerIndex[followee] = (me.followerIndex[followee][0], me.followerIndex[followee][1], False, True)
			except KeyError:
				k = 0
		i += 1
	element = driver.find_element_by_xpath(xpathDic["exitUserList"])
	element.click()

# Description: Utility funtion. Takes error message and writes it to log. Then alerts programmer.
# Parameters: error - string, error message
def logError(error):
	if os.path.exists("output.log"):
		with open("output.log", "a") as file:
			file.write(error+"\n")
	else:
		with open("output.log", "w") as file:
			file.write(error+"\n")
	print("ERROR: Check 'output.log' located in "+os.path.dirname(os.path.realpath("pynstagram_api.py"))+".")
