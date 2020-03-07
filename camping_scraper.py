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
def GetWebDriver_Chrome(chromedriver="/Applications/chromedriver", headless=True):
    """
    chrome driver --> path to chrome browser driver executable
    """

    CHROMEDRIVER_PATH = '/usr/bin/chromedriver'

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


#Point Reyes
old_url = 'https://www.recreation.gov/camping/campgrounds/233359'

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


# print(format_date(start_date))








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
                        preferred=None, blacklist=None):
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
    else:
        print('Available sites:')
        # for i, row in df.iterrows():
        print(df['Sites'])





#SCRIPT FOR NOTIFYING ME WHEN THERE IS AVAILABILITY
    #also inform me about refund policy


#CRON JOB THAT CONTINUALLY SEARCHES
    #appropriate interval between searches to avoid getting banned
    #randomize interval
    #interval between searching different campgrounds






def main(start_date, length_stay, url, preferred=None, blacklist=None):

    #Get Stay interval
    start_date, end_date = GetStayInterval(start_date, length_stay)

    #Get driver for web browser
    driver = GetWebDriver_Chrome(headless=False)


    df = CheckAvailability(driver, url, start_date, end_date,
                            preferred=preferred, blacklist=blacklist)

    PrintAvailableSites(df)

    # #close browser
    # driver.quit()
    print('NOT CLOSING BROWSER AT END FOR DEBUGGING')

if __name__ == "__main__":


    #SPECIFY CAMPING INTERVAL
    #start date and length of stay (nights)

    # #inputs
    # start_date = '2020-03-20'
    # length_stay = 2
    # URL = '{}/{}'.format(urls['recreation.gov'], campIDs['pointreyes'])

    # #text keywords of site names I dont want
    # Blacklist = [
    #                 'BOAT A',
    #                 'BOAT B',
    #                 'MARSHALL BEACH GROUP',
    #                 'TOMALES BEACH GROUP',
    #             ]

    # main(start_date=start_date, length_stay=length_stay, url=URL, blacklist=Blacklist)


    start_date = '2020-07-03'
    length_stay = 2
    URL = '{}/{}'.format(urls['recreation.gov'], campIDs['lassen_manzanita'])







    main(start_date=start_date, length_stay=length_stay, url=URL)





