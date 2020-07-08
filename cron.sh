#!/bin/sh


#######################################
# TO EDIT CRON JOBS, TYPE:
# crontab -e

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

#ADD THIS TO crontab TO RUN SCRAPER (AND UNCOMMENT):
# #campsite webscraper
# */5 * * * * cd ~/projects/personal/web_scraping/camping_scraper && ./cron.sh


#TO START CRON SERVICE
#sudo /etc/init.d/cron start
#TO STOP CRON SERVICE
#sudo /etc/init.d/cron stop

#######################################

#add to log file for debugging
echo `date` >> log.txt

#script that runs webscraper. called periodically by crontab
~/.pyenv/shims/python camping_scraper.py >> log.txt
# ./camping_scraper.py >> log.txt
