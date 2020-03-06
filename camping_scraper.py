from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
# import datetime
from datetime import datetime
import os
import time
import pandas as pd
url = 'https://www.recreation.gov/camping/aspen-hollow-group/r/campgroundDetails.do?contractCode=NRSO&parkId=71546'


#recreation.gov campground IDs

campIDs = {
            'pointreyes' : 233359,
            }

#Point Reyes
url = 'https://www.recreation.gov/camping/campgrounds/233359'

urls = {
    'recreation.gov' : 'https://www.recreation.gov/camping/campgrounds',
    }




start_date = '2020-03-13'
end_date   = '2020-03-22'


INPUT_DATE_FORMAT = "%Y-%m-%d"


def format_date(date, FMT="%Y-%m-%d"):
    date = datetime.strptime(date, FMT)
    date_formatted = datetime.strftime(date, "%Y-%m-%dT00:00:00Z")
    return date_formatted


print(format_date(start_date))



