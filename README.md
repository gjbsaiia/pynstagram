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

## setting up automated sheet
follow this tutorial to correctly configure your automated sheet and get your credentials</br>
- https://www.makeuseof.com/tag/read-write-google-sheets-python/
Credential need to be in .json format, titled "creds.json"</br>
Sheet can be titled however you like, but there needs to be three sub sheets, "RecentPost", "LikeListing", "Top10Followers"</br>
