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

# Define variables
DOCKER_CONTAINER_NAME = 'FCR_Wiki'
DOCKER_COMMAND_PATH = '/var/www/html'
BACKUP_FILE_DATE = time.strftime('%Y%m%d')
BACKUP_FILE_NAME = f"backup_{BACKUP_FILE_DATE}.sqlite"
DOCKER_BACKUP_PATH = f"{DOCKER_COMMAND_PATH}/backups/{BACKUP_FILE_NAME}"
DOCKER_COMMAND = f"php {DOCKER_COMMAND_PATH}/maintenance/run.php --server wiki.fogcityrocketry.com /var/www/html/maintenance/SqliteMaintenance.php --backup-to {DOCKER_BACKUP_PATH}"

# Run PHP SQLite maintenance script inside Docker container
EXIT_CODE_ONE = subprocess.call(['sudo', 'docker', 'exec', DOCKER_CONTAINER_NAME, DOCKER_COMMAND])

# Copy backup file to host
EXIT_CODE_TWO = subprocess.call(['sudo', 'docker', 'cp', DOCKER_BACKUP_PATH, f"~/backups/{BACKUP_FILE_NAME}"])

# Log results
LOG_FILE = '~/logs/backup.log'
TIMESTAMP = time.strftime('%Y-%m-%d %H:%M:%S')
if EXIT_CODE_ONE == 0 and EXIT_CODE_TWO == 0:
    MESSAGE = TIMESTAMP + ' Backup successful.'
    subprocess.call(['echo', MESSAGE, '>>', LOG_FILE])
else:
    MESSAGE = TIMESTAMP + ' Backup failed.'
    subprocess.call(['echo', MESSAGE, '>>', LOG_FILE])
    sys.exit(1)
