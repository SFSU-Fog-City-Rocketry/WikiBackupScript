# WikiBackupScript
Script to automatically run backups for the Wiki.

This script is run on a crontask inside the FCR_Wiki GCloud Compute Engine VM. It is run every day at 3:00 AM.

Backups are stored under the `backups` director under the home folder. The backups are titled as `backup_<date>.sqlite`.

While the backups are underway, the wiki will be locked for editing to prevent data corruption. Editors may notice a small delay in saving their edits. Readers should be unaffected.

## Further Reading

- [Manual:SqliteMaintenance.php](https://www.mediawiki.org/wiki/Manual:SqliteMaintenance.php): Used to backup the database
- [Manual:Backing up a wiki](https://www.mediawiki.org/wiki/Manual:Backing_up_a_wiki)
- [Manual:Restoring a Wiki from Backup](https://www.mediawiki.org/wiki/Manual:Restoring_a_wiki_from_backup)
