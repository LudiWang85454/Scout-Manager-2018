# Scout-Manager-2018
Put searchFolder.py in Desktop folder.
Set searchFolder.py to run as cron. (run crontab -e) and add the following line:
*/1 * * * * /usr/bin/python /home/NAMEOFUSER/Desktop/searchFolder.py
