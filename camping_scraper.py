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

def CheckAvailability(driver, url, start_date, end_date):
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
    df = pd.DataFrame(data, columns=colname)
    print(df)



    #DETERMINE IF ANY (DESIRED) SITES ARE AVAILABLE FOR DESIRED DATE





    return

    camping_availability_dictionary={}
    for week in range(0,how_many_weeks_to_check):
        driver.get(url)
        time.sleep(time_delay)

        start_date = current_time + datetime.timedelta(days=week*7) + datetime.timedelta(days=weeks_from_now_to_look*7)
        end_date = start_date + datetime.timedelta(days=nights_stay)
        selectElem=driver.find_element_by_xpath('//*[@id="arrivalDate"]')
        selectElem.clear()
        selectElem.send_keys(start_date.strftime("%a %b %d %Y"))
        time.sleep(time_delay)
        selectElem.submit()
        time.sleep(time_delay)

        selectElem=driver.find_element_by_xpath('//*[@id="departureDate"]')
        selectElem.clear()
        selectElem.send_keys(end_date.strftime("%a %b %d %Y"))
        time.sleep(time_delay)
        selectElem.submit()
        time.sleep(time_delay)

        site_data = driver.find_elements_by_class_name('searchSummary')
        time.sleep(time_delay)

        property_data = []
    for i in site_data:
        if len(i.text) != 0:
             property_data.append(i.text)

        camping_availability_dictionary[start_date.strftime("%a %b %d %Y") + ' to ' + end_date.strftime("%a %b %d %Y")] = property_data

        time.sleep(time_delay)




def tableDataText(table):
    """Parses a html segment started with tag <table> followed
    by multiple <tr> (table rows) and inner <td> (table data) tags.
    It returns a list of rows with inner columns.
    Accepts only one <th> (table header/data) in the first row.
    """
    def rowgetDataText(tr, coltag='td'): # td (data) or th (header)
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]
    rows = []
    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append(rowgetDataText(tr, 'td') ) # data row
    return rows







#SCRIPT FOR NOTIFYING ME WHEN THERE IS AVAILABILITY
    #also inform me about refund policy


#CRON JOB THAT CONTINUALLY SEARCHES
    #appropriate interval between searches to avoid getting banned
    #randomize interval
    #interval between searching different campgrounds



def main(start_date, length_stay):

    #Get Stay interval
    start_date, end_date = GetStayInterval(start_date, length_stay)

    #Get driver for web browser
    driver = GetWebDriver_Chrome(headless=False)


    CheckAvailability(driver, url, start_date, end_date)

    # #close browser
    # driver.quit()

if __name__ == "__main__":


    #SPECIFY CAMPING INTERVAL
    #start date and length of stay (nights)

    #inputs
    start_date = '2020-03-20'
    length_stay = 2







    main(start_date, length_stay)





