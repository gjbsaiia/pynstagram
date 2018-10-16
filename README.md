# pynstagram
Python API using selenium that scrapes data from your account</br>
-- work in progress... bear w me</br>
currently all functionality works for Ubuntu</br>
## Coming features
  - Hashtags that target your audience
  - Graphics
  
## This program requires the following installs:
  - python 2.7 (prob already have this)
  - chromedriver: https://launchpad.net/ubuntu/bionic/+package/chromium-chromedriver
  - selenium: "pip install selenium" (if you don't have pip, get pip)
  
## Setting up your login.txt file
Size refers to the size of your account. Accounts with followers/following less than 500 users can run "small",</br>
bigger accounts must run "big" so your requests are paced more slowly.</br>

Must be in the following format:</br>
Username = <your username></br>
Password = <passwd></br>
Size = [ big / small ]</br>

## Setting up automated sheet
GSheets are a great way to house and log your data.. </br>
You don't have to include this functionality, but bits of the API are set up to support it.</br>
follow this tutorial to correctly configure your automated sheet and get your credentials</br>
- https://www.makeuseof.com/tag/read-write-google-sheets-python/
Credential need to be in .json format, titled "creds.json"</br>
Sheet can be titled however you like, but there needs to be three sub sheets, "RecentPost", "LikeListing", "Top10Followers"</br>
