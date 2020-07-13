# Web Scraper for Reserving Campsites

## Usage
- Enter start date and length of stay in main `camping_scraper` script
    + eventually make input independent of this script
- Edit crontab to to run `cron.sh` (which runs camping scraper)
    + see `cron.sh` for more details

## Requirements
- Python modules (`pip install`...)
    + `bs4` (beautiful soup)
        * scraper
    + `lxml`
        * language for scraper
    + `selenium` 
        + webdriver
- Web driver (for selenium)
    - needs a driver program for your chosen webbrowser (e.g. chromedriver or geckodriver)
    - need to download this file for your machine
        + https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver
        + `sudo apt-get install chromium-chromedriver`

## Testing
- recreation.gov
    - point reyes 3/6/2020
    - lassen mansanita 3/6/2020


## TO DO
- Send batch email for multiple availabilities
- PR site 012 sending false positives
- Wrapper for checking multiple campsites
    - Run main multiple times
    - Generate single summary report
- Higher fidelity notification logger
    - Store dataframe of sites for which emails have been sent
    - Remove site if it has since become unavailable
- Scraper for reservecalifornia
