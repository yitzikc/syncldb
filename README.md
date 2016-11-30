# SyncLdb - a replicator of live LevelDB databases

SyncLdb is a Python3 script allowing the content of a LeveDB database to be accessed by multiple users.
This is accomplished by creating multiple replicas of LevelDB's directory structure, where the replicas use hard-links to
the files comprising the original database, except for the LOCK file, which isn't replicated. The replication goes on continuously until
the program is interrupted with Ctrl+C.

Note that no locking is provided. The user is advised to only access the LebelDB replicas for reading, however nothing is done to
enforce this.

_Usage_: `SyncLdb.py ldb_dir_path replica_dir_path`


# Requirements
- Python 3.4 or higher
- Watchdog package (see [installation instructions](http://pythonhosted.org/watchdog/installation.html#installation))

