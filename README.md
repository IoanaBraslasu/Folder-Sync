# Folder-Sync
This Python program maintains a full, identical copy of source folder at a replica folder.



## Libraries needed:
   Only built-in Python modules required:
* argparse
* os
* shutil
* time
* logging



## How does this program work?
Every user's operation of copying removal or updating in the source folder are logged to a file and to the console output. __Syncronization is performed periodically!__



There are 2 main functions:
1. __sync_folders__ function will perform the syncronization between given source and replica folders. Here the exact directory tree for both folders is created. Every change in the source folder is recorded in the log file

2. __log__ __creation__ function creates the log file and initialize the messages that shoul also appera on the console when onperations on the folder are performed 

## How to run this code?
Open your terminal and run the following bash command:

```bash
 python folder_sync.py /path/to/source /path/to/replica 60 /path/to/logfile.log

```
The command should contain the path to the source file and to the replica file, __syncronization__ __interval__  (e.g. 60->seconds)and the path to the log file.


