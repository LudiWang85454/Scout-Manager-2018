# Scout-Manager-2018
Put all scripts in Desktop folder (clone directly, move files out of auto-created folder into desktop).
Set searchFolder.py to run as cron. (run crontab -e) and add the following line:
*/1 * * * * /usr/bin/python /home/NAMEOFUSER/Desktop/searchFolder.py

Create directories 'data', 'sent' in 'Downloads' folder.
Run setup.py and update the file it creates.

Check configuration in databaseListener.py comments.
