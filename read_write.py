"""
Read and Write module for CSV interaction.
"""

from csv import DictWriter, reader
import os

LOG_FILE = "output_log.csv"


def read_csv(key_dict=None):
    """Read keystroke data from CSV file."""
    if key_dict is None:
        key_dict = {}
    
    if not os.path.exists(LOG_FILE):
        return key_dict
    
    with open(LOG_FILE, "r") as file:
        csv_file = reader(file)
        for row in csv_file:     
            key_dict[row[0]] = int(row[1])
    
    return key_dict


def write_csv(key_dict):
    """Write keystroke data to CSV file."""
    with open(LOG_FILE, "w", newline="") as file:
        fieldnames = ["Key", "timesPressed"]
        writer = DictWriter(file, fieldnames=fieldnames)
        for key in key_dict:
            writer.writerow({"Key": key, "timesPressed": key_dict[key]})


def update_key_count(key_dict, key):
    """Update the count for a specific key in the CSV file."""
    if key not in key_dict:
        key_dict[key] = 0
    write_csv(key_dict)