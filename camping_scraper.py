#!/usr/bin/env python
""" WEB SCRAPER FOR RESERVING CAMPSITES




RESOURCES:
https://alexmeub.com/finding-campsites-with-python/
    Beautiful Soup for html parsing, Mechanize for filling out web forms
    2015
https://towardsdatascience.com/web-scraping-basics-selenium-and-beautiful-soup-applied-to-searching-for-campsite-availability-4a8de1decac9
    Beautiful Soup for html, Selenium.webdriver for automating chrome
    2018
https://github.com/streeter/recreation-gov-campsite-checker
    Uses actual recreation.gov api
    2019
https://towardsdatascience.com/web-scraping-using-selenium-and-beautifulsoup-99195cd70a58
    more detail on selenium and beautifulsoup
"""



from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.firefox.options import Options
from random import randint
# import datetime
from datetime import datetime, timedelta
import os
import time
import pandas as pd

import platform


#script to send email notifications
import notify



########################################################################
### GENERAL USE UTILITIES AND DICTS
########################################################################


#Dict for reservation website urls
urls = {
        'recreation.gov' : 'https://www.recreation.gov/camping/campgrounds',
        }


#Dict for recreation.gov campground IDs
campIDs = {
            'pointreyes'       : 233359,
            'lassen_manzanita' : 234039
            }


def GetStayInterval(start, length, FMT="%Y-%m-%d"):
    #turn start date in datetime object
    start = datetime.strptime(start, FMT)
    #get end date
    end = start + timedelta(days=length)


    return start, end








def Touch(filename):
    """ Create an empty file named `filename`
    """
    open(filename, 'a').close()









# old_url = 'https://www.recreation.gov/camping/aspen-hollow-group/r/campgroundDetails.do?contractCode=NRSO&parkId=71546'

# #Point Reyes
# old_url = 'https://www.recreation.gov/camping/campgrounds/233359'


# INPUT_DATE_FORMAT = "%Y-%m-%d"








########################################################################
### WEBSCRAPING FUNCTIONS
########################################################################

def GetOS():
    platforms = {
        'Linux'   : 'Linux',
        'Darwin'  : 'macOS',
        'Windows' : 'Windows'
    }
    opsys = platforms[platform.system()]
    if opsys == 'Linux' and "microsoft" in platform.uname()[3].lower():
        #If on Windows Subsystem for Linux
        opsys = 'WSL'
    return opsys


def time_delay(tmin=1, tmax=2):
    """ Add a random time delay to act more like a human, avoid getting banned
    Randomly choose an integer amount of sections between the given range
    tmin/tmax: minimum/maximum amoun of seconds in delay
    """
    time.sleep(randint(tmin,tmax))

#SET UP WEB DRIVER
    #Selenium webdriver uses a web browser to navigate the web
    #needs a driver for the specific browser installed locally on your system

#chrome
def GetWebDriver_Chrome(chromedriver=None, headless=True):
    """
    chrome driver --> path to chrome browser driver executable
    """

    #Default locations for chromedriver
    if chromedriver is None:
        opsys = GetOS()
        if opsys == 'macOS':
            #macOS
            chromedriver="/Applications/chromedriver"
        elif opsys == 'Windows':
            #WINDOWS
            chromedriver="C:/Program Files (x86)/Google/Chrome/BrowserDriver/chromedriver.exe"
        elif opsys == 'WSL':
            #Windows Subsystem for Linux: drive chrome from the windows side
            chromedriver="/mnt/c/Program Files (x86)/Google/Chrome/BrowserDriver/chromedriver.exe"
        else:
            #LINUX
            #sudo apt-get install chromium-chromedriver
            chromedriver="/usr/lib/chromium-browser/chromedriver"

    if headless:
        WINDOW_SIZE = "1920,1080"
        # chrome_options = Options()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

        driver = webdriver.Chrome(executable_path=chromedriver,
                          options=chrome_options
                         )
    else:
        # os.environ["webdriver.chrome.driver"] = chromedriver
        # driver = webdriver.Chrome(chromedriver)

        driver = webdriver.Chrome(executable_path=chromedriver,)
    return driver


#firefox
def GetWebDriver_Firefox(browserdriver=None, headless=True):
    """
    browserdriver --> path to chrome browser driver executable
    """


    #Default locations for driver
    if browserdriver is None:
        opsys = GetOS()
        if opsys == 'macOS':
            #macOS
            browserdriver="/Applications/geckodriver"
        elif opsys == 'Windows':
            #WINDOWS
            browserdriver="/Applications/geckodriver"
        else:
            #LINUX
            #sudo apt-get install chromium-chromedriver
            browserdriver="/lib/BrowserDrivers/geckodriver"

    if headless:
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options, executable_path=browserdriver)

    else:

        driver = webdriver.Firefox(executable_path=browserdriver,)
    return driver



#SPECIFY DESIRED CAMPSITE
    #default: all/any site (return all)
    #blacklist: specific undesirable sites (e.g. group, ADA)
    #preferred: preferred sites

#SEARCH FOR CAMPSITE AVAILABILITY
    #

def GetAvailability(driver, url, start_date, end_date,
                        debug=False):
    """ Scrape website for campsite(s) are availability information between start/end dates.
    Return html soup from page that shows which sites are available
    This data can be reused for MULTIPLE stay intervals
    driver --> web browser driver
    url    --> url to desired campground
    """

    #Date format on recreation.gov
    FMT = "%m/%d/%Y"

    #OPEN CAMPGROUND URL
    driver.get(url)
    time_delay()

    #ENTER START DATE
        #right click on "Check In" web dialog and select "Inspect"
    #Find Start Date element by xpath with startDate keyword
    selectElem=driver.find_element_by_xpath('//*[@id="startDate"]')
    #clear current value
    selectElem.clear()
    #send desired start date value
    selectElem.send_keys(start_date.strftime(FMT))
    time_delay()
    # #submit?
    # selectElem.submit()
    # time_delay()


    #ENTER END DATE
        #same process as start date
    selectElem=driver.find_element_by_xpath('//*[@id="endDate"]')
    selectElem.clear()
    selectElem.send_keys(end_date.strftime(FMT))
    time_delay()
    # selectElem.submit()
    # time_delay()

    #NAVIGATE TO AVAILABILITY PAGE
    #Get "View by Availability" button element
    selectElem=driver.find_element_by_xpath('//*[@id="campground-view-by-avail"]')
    #click it
    selectElem.click()

    # #wait for everything on the page to load
    # element = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_id('iframe_container'))
    time_delay()





    ####################################
    #GET HTML SOUP FROM WEBPAGE
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # print(soup.prettify())

    return soup


def ProcessAvailability(soup, length_stay,
                        preferred=None, blacklist=None,
                        debug=False):
    """ Clean up html soup from website availability page
    Assess if any sites are available?
    preferred, blacklist --> campsite lists
    """

    #get campsite availability table
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="availability-table")




    #GET HEADERS FOR HTML TABLE (MAKE THIS OBJECT ORIENTED IN FUTURE)*****************

    #get column headers
        #find by right-click -> Inspect on web table cell with column header
        #find 'th' for header objects
        #class identifies specific object for col headers
        #stripped text is the text in the cell
    colname = [tx.text.strip() for tx in soup.find_all('th',
                attrs={'class' : "camp-sortable-column-header"}
                )]
    #only unique names
    tmp = list(colname)
    colname = list()
    for c in tmp:
        if c not in colname:
            #only add current value if it is not in list already
            colname.append(c)


    #get row headers
        #find by right-click -> Inspect on web table cell with campsite name in it
        #find 'th' for header objects
        #class identifies specific object for row headers
        #stripped text is the text in the cell
    rowname = [tx.text.strip() for tx in soup.find_all('th',
                attrs={'class' : "site-id-wrap camping-site-name-cell"}
                )]






    #GET BODY OF TABLE


    data = []
    #get just the body of the table
    table_body = table.find('tbody')
    #split by rows
    rows = table_body.find_all('tr')
    for row in rows:
        #split by columns
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols] #we just want the cell text
        data.append([ele for ele in cols if ele]) # Get rid of empty values
        # for col in cols:
        #     #we just want the cell text
        #     ele = col.text.strip()
        #     # Get rid of empty values
        #     if ele:
        #         data.append(ele)

    #PREPEND COLUMN FOR CAMPSITE NAME
    for i, row in enumerate(data):
        #for each row, add the rowname (campsite name) to the front
        data[i].insert(0, rowname[i])

    #Finalized table, with column headers
    dat = pd.DataFrame(data, columns=colname)


    #DOWNSELECT TABLE TO DESIRED STAY INTERVAL
        #1st col (0) is site name, 2nd col is "loop",
        #consequtive cols are increasing days, starting with start_date
    df = dat.iloc[:,0:length_stay+2] #plus 2 because extra col and zero indexing








    #DETERMINE IF ANY (DESIRED) SITES ARE AVAILABLE FOR DESIRED DATE



    if debug:
        print(df)

    #Get column names that correspond to days you will be staying
    depcols = df.columns.values[2:]
    print('NEED TO TEST THIS FOR ANOTHER CAMPSITE*******************************')

    #drop any row that has a reservation in stay interval
    for c in depcols:
        df = df.loc[(df[c] != 'R') & (df[c] != 'X')]


    if preferred is not None:
        #only check for availability in supplied sites
        print('Checking preferred sites only')
        for pr in preferred:
            print('    {}'.format(pr))

        #drop any remaining row that is blacklisted
        for i, row in df.iterrows():
            hits = [pr in row['Sites'] for pr in preferred]
            if not any(hits):
                #drop the row if none of the perferred sites match
                df = df.drop(i)

    elif blacklist is not None:
        #preferred is None, so any available except blacklist
        print('Checking all sites except:')
        for bl in blacklist:
            print('    {}'.format(bl))

        #drop any remaining row that is blacklisted
        for i, row in df.iterrows():
            for bl in blacklist:
                if bl in row['Sites']:
                    df = df.drop(i)

    else:
        #any available (already done)
        print('Checking all sites')

    return df


def PrintAvailableSites(df):
    """
    """

    if df.empty:
        print("No available sites :'(")
        availability = False
    else:
        print('Available sites:')
        # for i, row in df.iterrows():
        print(df['Sites'])
        availability = True

    return availability


def ReportAvailableSites(df, start_date=''):
    """
    """

    #initialize report with start of stay interval
    # report = ''
    report = '{}: '.format(start_date)

    if df.empty:
        availability = False

        report += "No available sites :'(\n"

    else:
        availability = True

        report += 'Available sites!!!:\n'
        for i, row in df.iterrows():
            report += '    {}\n'.format(row['Sites'])


    return report, availability




########################################################################
### EMAIL NOTIFICATION FUNCTIONS
########################################################################


def MakeSendAvailabilityReport(report, campground):


    #check if email is paused
    stillsend = CheckEmailPause()
    if not stillsend:
        print('Emails are paused: not sending')
        return


    #get current time, ignore millisecond
    now = datetime.now().replace(microsecond=0)
    now.strftime("%Y-%m-%d %H:%M:%S")
    #make email subject
    subject = 'Available Campsite: {} {}'.format(campground, now)
    #Send Email
    notify.main(subject, report)

    #ADD INFORMATION ABOUT *************************************************************************
        #STAY INTERVAL
        #BLACKLIST CAMPSITES


    #NEED A WAY TO PAUSE EMAILS IF A HIT IS FOUND*****************************************************


def CheckEmailPause():
    """ Pause emails if notification has already been sent so I dont get spammed
    """

    checkfile = 'pause.info'
    send_this_email = False

    if not os.path.exists(checkfile):
        #no email has been sent
        send_this_email = True

        # s = pd.Series({'email_pause' : True})
        # s.to_csv(checkfile, sep=' ')
        Touch(checkfile)
        return send_this_email
    else:
        return send_this_email

    # #otherwise, read the file
    # s = pd.read_csv(checkfile, sep=' ')

    # if s['email_pause']:
    #     #emails are paused, dont send
    #     return send_this_email
    # else:
    #     #send the email and dont send any afterwards
    #     send_this_email = True

    #     #pause all following emails
    #     s['email_pause'] = True
    #     s.to_csv(checkfile, sep=' ')

    #     return send_this_email



def CheckEmailPause_MoreFunctionality():
    """ Pause emails if notification has already been sent so I dont get spammed
    """

    checkfile = 'pause.info'
    send_this_email = False

    if not os.path.exists(checkfile):
        #no email has been sent
        send_this_email = True

        s = pd.Series({'email_pause' : True})
        s.to_csv(checkfile, sep=' ')
        return send_this_email

    #otherwise, read the file
    s = pd.read_csv(checkfile, sep=' ')

    if s['email_pause']:
        #emails are paused, dont send
        return send_this_email
    else:
        #send the email and dont send any afterwards
        send_this_email = True

        #pause all following emails
        s['email_pause'] = True
        s.to_csv(checkfile, sep=' ')

        return send_this_email







#SCRIPT FOR NOTIFYING ME WHEN THERE IS AVAILABILITY
    #also inform me about refund policy


#CRON JOB THAT CONTINUALLY SEARCHES
    #appropriate interval between searches to avoid getting banned
    #randomize interval
    #interval between searching different campgrounds






def main(start_date, length_stay,
            # url,
            website, campground,
            preferred=None, blacklist=None, debug=False):

    # start_dates = list([start_date]) if type(start_date) is not list else list(start_date)

    #GET CAMPGROUND URL
    url = '{}/{}'.format(urls[website], campIDs[campground])

    #GET STAY INTERVAL(s)
    start_date, end_date = GetStayInterval(start_date, length_stay)
    # sds, eds = [], []
    # for sd in start_dates:
    #     sd, ed = GetStayInterval(sd, length_stay)
    #     sds.append(sd)
    #     eds.append(ed)

    #GET DRIVER FOR WEB BROWSER
    headless = False if debug else True
    driver = GetWebDriver_Chrome(headless=headless)
    # driver = GetWebDriver_Firefox(headless=headless)

    #SCRAPE WEB FOR CAMPSITE AVAILABILITY
    soup = GetAvailability(driver, url, start_date, end_date,
                            debug=debug)
    df   = ProcessAvailability(soup, length_stay,
                            preferred=preferred, blacklist=blacklist,
                            debug=debug)
    #ASSESS AVAILABILITY
    # available = PrintAvailableSites(df)
    report, avail = ReportAvailableSites(df, start_date)
    print(report)

    #SEND EMAIL NOTIFICATION IF AVAILABLE SITES
    if avail:
        MakeSendAvailabilityReport(report, campground)



    # #get availability info for entire date range (assumes dates are given in chronological order*****************************8)
    # # dat = GetAvailability(driver, url, start_date, end_date,
    # #                         debug=debug)
    # dat = GetAvailability(driver, url, sds[0], eds[-1],
    #                         debug=debug)

    # #check availability for each stay interval
    # reports = ''
    # send = False
    # for sd in start_dates:
    #     #downselect availability to specific stay interval, desired sites
    #     df = ProcessAvailability(soup, sd, length_stay,
    #                             preferred=preferred, blacklist=blacklist,
    #                             debug=debug)

    #     #ASSESS AVAILABILITY
    #     # available = PrintAvailableSites(df)
    #     report, avail = ReportAvailableSites(df, sd)
    #     print(report)

    #     if avail:
    #         #if available site, add report outgoing email content
    #         reports = '{}\n\n{}'.format(reports, report)
    #         send = True

    # #SEND EMAIL NOTIFICATION IF AVAILABLE SITES
    # if send:
    #     MakeSendAvailabilityReport(reports, campground)











    #CLOSE BROWSER
    if debug:
        print('NOT CLOSING BROWSER AT END FOR DEBUGGING')
    else:
        driver.quit()


if __name__ == "__main__":


    # Touch('itran.txt')

    DEBUG = False
    # DEBUG = True

    #SPECIFY CAMPING INTERVAL
    #start date and length of stay (nights)


    #POINT REYES
    #inputs
    start_date  = '2020-03-21'
    start_dates  = ['2020-07-18', '2020-08-01', '2020-08-08', '2020-08-15', '2020-08-29', '2020-09-05', '2020-09-12', '2020-09-19', '2020-09-26',]
    length_stay = 1
    # URL = '{}/{}'.format(urls['recreation.gov'], campIDs['pointreyes'])
    Campground = 'pointreyes'
    Website    = 'recreation.gov'

    #text keywords of site names I dont want
    Blacklist = [
                    'BOAT A',
                    'BOAT B',
                    'MARSHALL BEACH GROUP',
                    'TOMALES BEACH GROUP',
                ]


    # main(start_date=start_dates, length_stay=length_stay,
    #             # url=URL,
    #             website=Website, campground=Campground,
    #             blacklist=Blacklist, debug=DEBUG)
    for start_date in start_dates:
        main(start_date=start_date, length_stay=length_stay,
                # url=URL,
                website=Website, campground=Campground,
                blacklist=Blacklist, debug=DEBUG)


    # #LASSEN MANSANITA
    # start_date = '2020-07-03'
    # length_stay = 2
    # URL = '{}/{}'.format(urls['recreation.gov'], campIDs['lassen_manzanita'])

    # main(start_date=start_date, length_stay=length_stay, url=URL)





