#!/usr/bin/python

# Griffin Saiia, gjs64@case.edu
# github: https://github.com/gjbsaiia

import os
import sys
from datetime import datetime, timedelta, date
import json
from oauth2client.client import SignedJwtAssertionCredentials
#my Libraries
from instaDictionaries import myMonths

class profile: # object the encloses all your data
	def __init__(self):
		self.creds = "creds.json" # API Key to optional Google Sheet functionality
		self.credentials = "" # signed, formated credentials
		self.login = "login.txt" # path to your login information
		self.username = "" # user this object represents
		self.password = "" # password for this account
		self.size = False
		self.sheetName = "" # Google Sheet Name (optional)
		self.followerIndex = {} # follower[<username>]=(<Posts_Liked>, <Comments_Liked>, <Are_Following>, <Unfollowed>)
		self.numFollowers = 0 # number of followers
		self.followers = []
		self.numFollowing = 0 # number profile is following
		self.following = []
		self.shitList = [] # Ghosts/NonFollowBackers, people you may want to unfollow
		self.start = 0 # time script started running
		self.stop = 0 # time script stopped running
		self.totalTime = "" # total time script ran as formated string
		self.recentPosts = [] # array containing photoAnalytics objects
		self.top10 = [] # array containing the usernames of your top 10 followers
	def configCreds(self):
		if os.path.exists(self.creds):
			json_key = json.load(open(self.creds))
			scopeList = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
			self.credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scopeList)
	def defNumFollowers(self, num):
		self.numFollowers = int(num)
	def addFollower(self, follower):
		self.followers.append(follower)
	def defNumFollowing(self, num):
		self.numFollowing = int(num)
	def addFollowee(self, followee):
		self.following.append(followee)
	def defaultShitList(self):
		self.shitlist = list(set(self.following) - set(self.followers))
	def addToShitList(self, list): # adds list to shitlist
		self.shitList += list
	def addPost(self, currentPost): # adds post object to recentPosts array
		self.recentPosts.append(currentPost)
	def addTop(self, follower): # defines top 10 list
		self.top10.append(follower)
	def startTime(self): # starts the clock
		sta = datetime.now()
		self.start = timedelta(hours=sta.hour,minutes=sta.minute,seconds=sta.second)
	def stopTime(self): # stops the clock
		sto = datetime.now()
		self.stop = timedelta(hours=sto.hour,minutes=sto.minute,seconds=sto.second)
		self.totalTime = str(self.stop-self.start)
class post: # object to enclose all data concerning one post
	def __init__(self, me):
		self.parent = me # profile this post belongs to
		self.likers = [] # usernames for all users who have liked
		self.commenters = [] # usernames for all users who have commented
		self.numLikes = 0 # number of likes
		self.numComments = 0 # number of comments
		self.caption = "" # caption
		self.date = "" # date post was posted
	def addLiker(self, liker): # adds liker to likers
		self.likers.append(liker)
	def addCommenter(self, commenter): # adds commenter to commenters
		self.commenters.append(commenter)
	def defNumLikes(self, num): # defines number of likes
		self.numLikes = int(num)
	def defNumComments(self, num): # defines number of comments
		self.numComments = int(num)
	def defTime(self, string): # defines time as date object
		dt = string.split(" ")
		self.date = date(int(dt[2]), myMonths[dt[0]], int(dt[1].strip(",")[0]))
	def defCaption(self, string): # defines caption
		self.caption = string
