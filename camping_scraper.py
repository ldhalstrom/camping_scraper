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
from random import randint
# import datetime
from datetime import datetime, timedelta
import os
import time
import pandas as pd

import platform


#script to send email notifications
import notify


def GetOS():
    platforms = {
        'Linux'   : 'Linux',
        'Darwin'  : 'macOS',
        'Windows' : 'Windows'
    }
    return platforms[platform.system()]


def time_delay(tmin=1, tmax=2):
    """ Add a random time delay to act more like a human, avoid getting banned
    Randomly choose an integer amount of sections between the given range
    tmin/tmax: minimum/maximum amoun of seconds in delay
    """
    time.sleep(randint(tmin,tmax))


def Touch(filename):
    """ Create an empty file named `filename`
    """
    open(filename, 'a').close()


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
        if opsys == 'Darwin':
            #macOS
            chromedriver="/Applications/chromedriver"
        elif opsys == 'Windows':
            #WINDOWS
            print('NEED UPDATED CHROMEDRIVER PATH FOR WINDOWS')
            chromedriver="/Applications/chromedriver"
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






old_url = 'https://www.recreation.gov/camping/aspen-hollow-group/r/campgroundDetails.do?contractCode=NRSO&parkId=71546'


#recreation.gov campground IDs

campIDs = {
            'pointreyes'       : 233359,
            'lassen_manzanita' : 234039
            }

urls = {
        'recreation.gov' : 'https://www.recreation.gov/camping/campgrounds',
        }



#Point Reyes
old_url = 'https://www.recreation.gov/camping/campgrounds/233359'







INPUT_DATE_FORMAT = "%Y-%m-%d"





def GetStayInterval(start, length, FMT="%Y-%m-%d"):
    #turn start date in datetime object
    start = datetime.strptime(start, FMT)
    #get end date
    end = start + timedelta(days=length)


    return start, end








#SPECIFY DESIRED CAMPSITE
    #default: all/any site (return all)
    #blacklist: specific undesirable sites (e.g. group, ADA)
    #preferred: preferred sites

#SEARCH FOR CAMPSITE AVAILABILITY
    #

def CheckAvailability(driver, url, start_date, end_date,
                        preferred=None, blacklist=None, debug=False):
    """ Check if campsite(s) are available
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

    #column names that correspond to days of stay
    depcols = df.columns.values[2:]

    print('NEED TO TEST THIS FOR ANOTHER CAMPSITE*******************************')






    #DETERMINE IF ANY (DESIRED) SITES ARE AVAILABLE FOR DESIRED DATE



    if debug:
        print(df)

    #drop any row that has a reservation in stay interval
    for c in depcols:
        df = df.loc[(df[c] != 'R') & (df[c] != 'X')]


    if preferred is not None:
        #only check for availability in supplied sites
        print('Checking preferred sites only')

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


def ReportAvailableSites(df):
    """
    """

    report = ''

    if df.empty:
        availability = False

        report += "No available sites :'(\n"

    else:
        availability = True

        report += 'Available sites!!!:\n'
        for i, row in df.iterrows():
            report += '    {}\n'.format(row['Sites'])


    return report, availability



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

    #GET CAMPGROUND URL
    url = '{}/{}'.format(urls[website], campIDs[campground])

    #GET STAY INTERVAL
    start_date, end_date = GetStayInterval(start_date, length_stay)

    #GET DRIVER FOR WEB BROWSER
    headless = True if debug else False
    driver = GetWebDriver_Chrome(headless=headless)

    #SCRAPE WEB FOR CAMPSITE AVAILABILITY
    df = CheckAvailability(driver, url, start_date, end_date,
                            preferred=preferred, blacklist=blacklist,
                            debug=debug)

    #ASSESS AVAILABILITY
    # available = PrintAvailableSites(df)
    report, avail = ReportAvailableSites(df)
    print(report)


    #SEND EMAIL NOTIFICATION IF AVAILABLE SITES
    if avail:
        MakeSendAvailabilityReport(report, campground)











    #CLOSE BROWSER
    if debug:
        print('NOT CLOSING BROWSER AT END FOR DEBUGGING')
    else:
        driver.quit()


if __name__ == "__main__":


    # Touch('itran.txt')

    DEBUG = False
    DEBUG = True

    #SPECIFY CAMPING INTERVAL
    #start date and length of stay (nights)


    #POINT REYES
    #inputs
    start_date  = '2020-03-20'
    length_stay = 2
    # URL = '{}/{}'.format(urls['recreation.gov'], campIDs['pointreyes'])
    Campground = 'pointreyes'
    Website    = 'recreation.gov'

    #text keywords of site names I dont want
    Blacklist = [
                    'BOAT A',
                    # 'BOAT B',
                    # 'MARSHALL BEACH GROUP',
                    # 'TOMALES BEACH GROUP',
                ]

    main(start_date=start_date, length_stay=length_stay,
            # url=URL,
            website=Website, campground=Campground,
            blacklist=Blacklist, debug=DEBUG)


    # #LASSEN MANSANITA
    # start_date = '2020-07-03'
    # length_stay = 2
    # URL = '{}/{}'.format(urls['recreation.gov'], campIDs['lassen_manzanita'])

    # main(start_date=start_date, length_stay=length_stay, url=URL)





