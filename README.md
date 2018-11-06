# pynstagram
Python API using selenium that scrapes data from your account</br>
Also allows you to unfollow targeted accounts (non-follow-backers, ghost accounts)</br>
Functionality for Ubuntu</br>

## Update
Facebook has been mutating their html structure most weeks, this makes upkeep exhausting. </br>
This project has lost a lot of its appeal for me, so I won't be maintaining this tool. </br>
All the code here is valid, and works - all that needs to be changed are the xpaths stored in</br>
instaDictionaries.py. Typically the only change in htmml is an extra "< div >". </br>
Hope someone else can have as much fun as I did with this project!</br>
  
## This program requires the following installs:
  - python 2.7 (prob already have this)
  - chromedriver: https://launchpad.net/ubuntu/bionic/+package/chromium-chromedriver
  - selenium: "pip install selenium" (if you don't have pip, get pip)
  
## Setting up your login.txt file
Size refers to the size of your account. Accounts with followers/following less than 500 users can run "small",</br>
bigger accounts must run "big" so your requests are paced more slowly.</br>

Must be in the following format:</br>
Username = usernom</br>
Password = password</br>
Size = [ big / small ]</br>

## Setting up automated sheet
GSheets are a great way to house and log your data.. </br>
You don't have to include this functionality, but bits of the API are set up to support it.</br>
follow this tutorial to correctly configure your automated sheet and get your credentials</br>
- https://www.makeuseof.com/tag/read-write-google-sheets-python/
Credential need to be in .json format, titled "creds.json"</br>
Sheet can be titled however you like, but there needs to be three sub sheets, "RecentPost", "LikeListing", "Top10Followers"</br>

## Example Script
I've included the data scraping bot I use with my API. Shows how I incorporated google sheets.</br>
If you set up your Google Sheet with the instructions in the tutorial above, you can run my example.</br>
