"""
Loggable Class

This module defines a Loggable class that provides a simple logging mechanism.
Logs can be added using the log method, and the logs can be retrieved or saved to a file.

Author: Haydens Little Helpers
Date: 23/11/2023

Usage:
    # Create an instance of the Loggable class
    logger = Loggable()

    # Add logs
    logger.log("Log entry 1")
    logger.log("Log entry 2")

    # Get logs
    all_logs = logger.logs

    # Save logs to a file
    logger.save_logs_to_file("logfile.txt")
"""

class Loggable:
    def __init__(self):
        self._logs = []

    def log(self, message):
        """
        Add a log entry to the list.

        :param message: The log message to be added.
        """
        if isinstance(message, str):
            self._logs.append(message)

    @property
    def logs(self):
        """
        Retrieve the list of logs.

        :return: A list of log entries.
        """
        return self._logs

    def save_logs_to_file(self, filename):
        """
        Save logs to a file.

        :param filename: The name of the file to save the logs to.
        """
        with open(filename, 'w') as file:
            for log_entry in self.logs:
                file.write(log_entry + '\n')