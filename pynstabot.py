#!/usr/bin/python

# Griffin Saiia, gjs64@case.edu
# github: https://github.com/gjbsaiia

import os
import sys
import time
import gspread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# my Libraries
from instaDictionaries import xpathDic
from classDefinitions import profile
from classDefinitions import post
import pynstagram_api as api

def main():
	me = profile()
	api.unpackMe(me)
	driver = api.start(me, True)
	api.scrapeSelf(me, driver)
	file = gspread.authorize(me.credentials)
	recentPost = file.open(me.sheetName).get_worksheet(0)
	last = recentPost.cell(1,2).value
	if(last == ""):
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpathDic["postCount"])))
		element = driver.find_element_by_xpath(xpathDic["postCount"])
		try:
			n = int(element.text)
		except ValueError:
			split = element.text.split(",")
			num = split[0]+split[1]
			n = int(num)
		me = api.scrapeNumberOfPosts(me, driver, n, True)
	else:
		me = api.scrapePostsToDate(me, driver, last)
	file = gspread.authorize(me.credentials)
	recentPost = file.open(me.sheetName).get_worksheet(0)
	try:
		analyzeRecentPost(recentPost, me)
	except IndexError:
		print("Sheet is updated")
		return 0
	file = gspread.authorize(me.credentials)
	likeListing = file.open(me.sheetName).get_worksheet(1)
	updateDic(me, likeListing)
	time.sleep(100)
	file = gspread.authorize(me.credentials)
	top10Followers = file.open(me.sheetName).get_worksheet(2)
	api.getTop10(me)
	api.addGhostsToShitList(me)
	writeTop10(me, top10Followers)
	#api.unfollow(me, driver)
	driver.close()
	time.sleep(100)
	file = gspread.authorize(me.credentials)
	likeListing = file.open(me.sheetName).get_worksheet(1)
	writeLikeListing(me, likeListing)
	time.sleep(100)
	me.stopTime()
	file = gspread.authorize(me.credentials)
	recentPost = file.open(me.sheetName).get_worksheet(0)
	markScriptRan(recentPost, me)
	return 0

def analyzeRecentPost(recentPost, me):
	requests = 0
	post = me.recentPosts[0]
	date = str(post.date.month)+"/"+str(post.date.day)+"/"+str(post.date.year)
	recentPost.update_cell(1,2,date)
	requests += 1
	input = post.caption
	recentPost.update_cell(2,2,input)
	requests += 1
	input = post.numLikes
	recentPost.update_cell(3,2,input)
	requests += 1
	input = post.numComments
	recentPost.update_cell(4,2,input)
	requests += 1
	i = 6
	j = 6
	k = 6
	nonFollowers = []
	for liker in post.likers:
		if(requests > 90):
			requests = 0
			time.sleep(100)
		try:
			test = me.followerIndex[liker]
			recentPost.update_cell(i, 1, liker)
			requests += 1
			i += 1
		except KeyError:
			recentPost.update_cell(k, 3, liker)
			nonFollowers.append(liker)
			requests += 1
			k += 1
	for commenter in post.commenters:
		if(requests > 90):
			requests = 0
			time.sleep(100)
		try:
			test = me.followerIndex[commenter]
			recentPost.update_cell(j, 2, commenter)
			requests += 1
			j += 1
		except KeyError:
			if commenter not in nonFollowers:
				recentPost.update_cell(i, 3, commenter)
				nonFollowers.append(commenter)
				requests += 1
				k += 1

def updateDic(me, likeListing):
	i = 2
	while(likeListing.cell(i,1).value != ""):
		reads += 1
		if(reads > 90):
			reads = 0
			time.sleep(100)
		user = likeListing.cell(i,1).value
		reads += 1
		try:
			test = me.followerIndex[user]
			reads += 1
			currentLikes = int(likeListing.cell(i,2).value)
			reads += 1
			currentComments = int(likeListing.cell(i,3).value)
			reads += 1
			me.followerIndex[user] = (currentLikes+me.followerIndex[user][0], currentComments+me.followerIndex[user][1], me.followerIndex[user][2], me.followerIndex[user][3])
		except KeyError:
			k = 0

def writeTop10(me, top10Followers):
	i = 2
	for each in me.top10:
		top10Followers.update_cell(i,2,each)
		top10Followers.update_cell(i,3,me.followerIndex[each][0])
		top10Followers.update_cell(i,4,me.followerIndex[each][1])
		top10Followers.update_cell(i,5,me.followerIndex[each][2])
		i += 1

def writeLikeListing(me, likeListing):
	writes = 0
	reads = 0
	reads += 1
	if(likeListing.cell(2,1).value == ""):
		i = 2
		for key in me.followerIndex:
			likeListing.update_cell(i, 1, key)
			writes += 1
			input = str(me.followerIndex[key][0])
			likeListing.update_cell(i, 2, input)
			writes += 1
			input = str(me.followerIndex[key][1])
			likeListing.update_cell(i, 3, input)
			writes += 1
			input = str(me.followerIndex[key][2])
			likeListing.update_cell(i, 4, input)
			writes += 1
			input = str(me.followerIndex[key][3])
			likeListing.update_cell(i, 5, input)
			writes += 1
			i += 1
			if(writes > 90):
				writes = 0
				time.sleep(100)
	else:
		i = 2
		listedUsers = []
		while(likeListing.cell(i,1).value != ""):
			reads += 1
			if(writes > 90 or reads > 90):
				writes = 0
				reads = 0
				time.sleep(100)
			user = likeListing.cell(i,1).value
			listedUsers.append(user)
			reads += 1
			currentLikes = likeListing.cell(i,2).value
			reads += 1
			currentComments = likeListing.cell(i,3).value
			reads += 1
			try:
				test = me.followerIndex[user]
				input = str(currentLikes+me.followerIndex[user][0])
				likeListing.update_cell(i,2, input)
				writes += 1
				input = str(currentComments+me.followerIndex[user][1])
				likeListing.update_cell(i,3,input)
				writes += 1
				input = str(me.followerIndex[user][2])
				likeListing.update_cell(i,4,input)
				writes += 1
				input = str(me.followerIndex[user][3])
				likeListing.update_cell(i,5,input)
				writes += 1
				me.followerIndex[user] = (currentLikes+me.followerIndex[user][0], currentComments+me.followerIndex[user][1], me.followerIndex[user][2], me.followerIndex[user][3])
			except KeyError:
				likeListing.update_cell(i,5,"True")
				writes += 1
			i += 1
		reads += 1
		if(len(listedUsers) != len(me.followerIndex)):
			while(likeListing.cell(i,1).value != ""):
				i += 1
				reads += 1
				if(writes > 90 or reads > 90):
					writes = 0
					reads = 0
					time.sleep(100)
			reads += 1
			for key in me.followerIndex:
				if(writes > 90 or reads > 90):
					writes = 0
					reads = 0
					time.sleep(100)
				if key not in listedUsers:
					likeListing.update_cell(i, 1, key)
					writes += 1
					input = str(me.followerIndex[key][0])
					likeListing.update_cell(i, 2, input)
					writes += 1
					input = str(me.followerIndex[key][1])
					likeListing.update_cell(i, 3, input)
					writes += 1
					input = str(me.followerIndex[key][2])
					likeListing.update_cell(i, 4, input)
					writes += 1
					input = str(me.followerIndex[key][3])
					likeListing.update_cell(i, 5, input)
					writes += 1
					i += 1

def markScriptRan(recentPost, me):
	recentPost.update_cell(1,4, "True")
	recentPost.update_cell(3,4, me.totalTime)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
