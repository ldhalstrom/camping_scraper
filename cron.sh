#!/bin/sh

#add to log file for debugging
echo `date` >> log.txt

#script that runs webscraper. called periodically by crontab
/Users/lhalstro/.pyenv/shims/python camping_scraper.py >> log.txt
