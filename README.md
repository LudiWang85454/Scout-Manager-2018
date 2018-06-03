# Scout-Manager-2018
The system is designed to run on an Ubuntu computer and is fully automated using systemctl.
This year, with the implementation of the new bluetooth system and the new QR system, these
scripts could not be implemented into the server due to time constraints, so they were separated
into "Scout-Manager".  Scout-Manager deals with all bluetooth and QR systems, and diagnostics
and missing data.

scheduler.py runs other scripts that run on a regular interval
databaseListener.py runs other scripts based on events on our database
(events include change in match number or scout rotation - called a cycle)

Setup:
Put all scripts in ~/scoutManager folder (clone directly, move files out of auto-created folder into scoutManager). (Use cp -a to move files) (create the 'scoutManager' folder with mkdir)

Run setup.py.