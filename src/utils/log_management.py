#!/usr/bin/env python3


from datetime import datetime


def write_log(log, current_month):
    """
    Write the files to the log
    """
    with open(f"./logs/{current_month}-log.txt", "a") as f:
        for month, files in log.items():
            for file_name in files:
                f.write(f"\t{file_name}\n")
                f.write("\n")
            print(f"Saved log: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n")