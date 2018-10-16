#!/usr/bin/python

# Griffin Saiia, gjs64@case.edu
# github: https://github.com/gjbsaiia

xpathDic = { # xPaths to various locations on the instagram website
"user":"//*[@name='username']", # username input
"password":"//*[@name='password']", # password input
"submit":"/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/button", #submit button
"notif":"/html/body/div[2]/div/div/div/div[3]/button[2]", # Notification message exit
"trickyNotif":"/html/body/div[3]/div/div/div/div[3]/button[2]", # Facebook sometimes adds adition div
"profile":"//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[3]/a", # profile home
"followers":"//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a", # link to follower listing
"followersCount":"//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span", # number of followers
"postCount":"//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span", # number of posts
"following":"//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a", # link to following listing
"followingCount":"//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span", # number of people you're following
"userFrame":"/html/body/div[3]/div/div/div[2]", # div frame for follower/following listing
"userList":"/html/body/div[3]/div/div/div[2]/ul/div/li", # seed xpath for each follower/followee, allows for running count
"userPt1":"/html/body/div[3]/div/div/div[2]/ul/div/li[", # first half of a follower/followee xpath
"userPt2":"]/div/div[1]/div[2]/div[1]/a", # second half of a follower/followee xpath that gives username
"userUnfollow":"]/div/div[2]/button", # second half of a follower/followee xpath that gives their unfollow button
"unfollow":"/html/body/div[4]/div/div/div/div[3]/button[1]", # button to confirm unfollow
"exituserList":"/html/body/div[3]/div/div/div[1]/div[2]/button/span", # button to exit follow/followee listing
"picFrame":"/html/body/div[3]/div/div[2]/div/article", # div frame containing posts
"pic1":"//*[@id='react-root']/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a", # path to first post
"next":"/html/body/div[3]/div/div[1]/div/div/a", # path to second post from first post
"nextt":"/html/body/div[3]/div/div[1]/div/div/a[2]", # path to every subsequent post following second post
"exitPics":"/html/body/div[3]/div/button", # button to exit pictures
"time":"/html/body/div[2]/div/div[2]/div/article/div[2]/div[2]/a/time", # path to timestamp for each post
"trickyTime":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/a/time", # Facebook sometimes adds additional div
"deepTime":"/html/body/div[3]/div/div[2]/div/article/div[2]/div/a/time", # past 40 posts deep this path changes
"caption":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span", # path to caption of post
"likes":"/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/button", # path to lisitng of users that have liked
"numLikes":"/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/button/span", # number of likes on post
"likerFrame":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]", # div frame for liking users listing
"likerList":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li", # seed xpath for each user that has liked
"likerPt1":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li[", # first half of liker's xpath
"likerPt2":"]/div/div[1]/div[2]/div[1]/a", # second half of liker's xpath pointing to username
"exitlikerList":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/button/span", # path to exit button to leave likes
"commenterList":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li", # seed xpath for commenter
"loadMore":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/button", # load more button to ensure we have full list of commenters
"noCaptionLoadMore":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/button", # no caption moves load more button
"commenterPt1":"/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[", # first half of commenter's xpath
"commenterPt2":"]/div/div/div/a" # second half of commenters xpath that points to username
}

myMonths = { # lazy way to handle abreviations used by Facebook for post timestamps
"Jan":1,
"Feb":2,
"Mar":3,
"Apr":4,
"May":5,
"Jun":6,
"Jul":7,
"Aug":8,
"Sep":9,
"Oct":10,
"Nov":11,
"Dec":12
}
