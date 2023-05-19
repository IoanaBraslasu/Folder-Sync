import argparse
import os
import shutil
import time
import logging


def sync_folders(source_folder, replica_folder, log_file):
    # Sync files from source to replica folder:
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            replica_path = os.path.join(replica_folder, os.path.relpath(source_path, source_folder))
            replica_dir = os.path.dirname(replica_path)

            # Create sub-folders in replica folder as in the source folder:
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)

            # Copying the existing files from source folder to replica:
            if not os.path.exists(replica_path) or os.stat(source_path).st_mtime > os.stat(replica_path).st_mtime:
                shutil.copy2(source_path, replica_path)
                log_file.info("Copied file: %s", replica_path)

            # If an existing copied file in replica is updated in source folder:
            elif os.stat(source_path).st_mtime < os.stat(replica_path).st_mtime:
                shutil.copy2(replica_path, source_path)
                log_file.info("Updated file in source folder: %s", source_path)

    # Remove files from replica folder that don't exist in the source folder:
    for root, dirs, files in os.walk(replica_folder):
        for file in files:
            replica_path = os.path.join(root, file)
            source_path = os.path.join(source_folder, os.path.relpath(replica_path, replica_folder))
            if not os.path.exists(source_path):
                os.remove(replica_path)
                log_file.info("Removed file: %s", replica_path)


def log_creation(source_folder, replica_folder, log_file):
    # Create the log file handler:
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s %(message)s')

    # Create a console handler to log to console output:
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logging.getLogger('').addHandler(console)

    # Get the logger instance:
    logger = logging.getLogger(__name__)

    # Log initial synchronization:
    logger.info("Initial synchronization started.")

    # Perform initial synchronization:
    sync_folders(source_folder, replica_folder, logger)

    # Start periodic synchronization:
    while True:
        time.sleep(interval)
        sync_folders(source_folder, replica_folder, logger)


if __name__ == '__main__':
    # Creating an object to define and handle command-line arguments:
    parser = argparse.ArgumentParser(description='Folder synchronization program')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')
    parser.add_argument('replica_folder', type=str, help='Path to the replica folder')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, help='Path to the log file')

    # Parses the command-line arguments
    args = parser.parse_args()

    # Retrieve the values of the command-line arguments and assign them to variables in the code:
    source = args.source_folder
    replica = args.replica_folder
    interval = args.interval
    log = args.log_file

    if not os.path.exists(replica):
        # Creating the replica folder if it doesn't exist with the specified name:
        os.makedirs(replica)
        # Set the replica folder the permission to make it writable:
        os.chmod(replica, 0o777)

    log_creation(source, replica, log)
