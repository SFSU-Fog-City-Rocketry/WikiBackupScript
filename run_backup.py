# Steps:
# Run PHP SQLite maintenance script inside Docker container
#   docker exec FCR_Wiki php /var/www/html/maintenance/run.php --server wiki.fogcityrocketry.com /var/www/html/maintenance/SqliteMaintenance.php --backup-to /var/www/html/backups/backup.sqlite
# Copy backup file to host
#   docker cp FCR_Wiki:/var/www/html/data/backup.sqlite ~/backups/backup_[date].sqlite
#   date format is YYYYMMDD
# Log results to ~/logs/backup.log

# During backups, the wiki is read-only. Given the small size of the wiki, this
# should only result in a few seconds of delay for editors. Readers should be
# unaffected.

# Reference: https://www.mediawiki.org/wiki/Manual:SqliteMaintenance.php

# Import modules
import subprocess
import sys
import time
import logging

# Define variables
DOCKER_CONTAINER_NAME = 'FCR_Wiki'
BACKUP_FILE_DATE = time.strftime('%Y%m%d')
BACKUP_FILE_NAME = f"backup_{BACKUP_FILE_DATE}.sqlite"
DOCKER_BACKUP_PATH = f"/var/www/html/backups/{BACKUP_FILE_NAME}"
DOCKER_COMMAND = f"php /var/www/html/maintenance/run.php --server wiki.fogcityrocketry.com /var/www/html/maintenance/SqliteMaintenance.php --backup-to /var/www/html/backups/{BACKUP_FILE_NAME}"
HOME_DIRECTORY = '/home/ethanhanlon'

# Run PHP SQLite maintenance script inside Docker container
EXIT_CODE_ONE = subprocess.call(
    [
        'sudo', 
        'docker', 
        'exec', 
        "FCR_Wiki", 
        "php",
        "/var/www/html/maintenance/run.php",
        "--server",
        "wiki.fogcityrocketry.com",
        "/var/www/html/maintenance/SqliteMaintenance.php",
        "--backup-to",
        DOCKER_BACKUP_PATH
    ]
)

# Copy backup file to host
EXIT_CODE_TWO = subprocess.call(
    [
        'sudo',
        'docker',
        'cp',
        f"FCR_Wiki:{DOCKER_BACKUP_PATH}",
        f"{HOME_DIRECTORY}/backups/{BACKUP_FILE_NAME}"
    ]
)

# Log results
logging.basicConfig(filename=f"{HOME_DIRECTORY}/backups/backup.log", level=logging.DEBUG)
TIMESTAMP = time.strftime('%Y-%m-%d %H:%M:%S')

MESSAGE = f"\"{TIMESTAMP} Backup successful.\"" if EXIT_CODE_ONE == 0 and EXIT_CODE_TWO == 0 else f"\"{TIMESTAMP} Backup failed.\""

logging.info(MESSAGE)

sys.exit(0 if EXIT_CODE_ONE == 0 and EXIT_CODE_TWO == 0 else 1)
