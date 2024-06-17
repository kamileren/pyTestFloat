#floatGenerator.py

import threading
import time
import random
import csv
from datetime import datetime


class FloatGenerator(threading.Thread):

    def __init__(self, filename = 'float.csv',minutes = 5,secondperfloat = 5):

        super().__init__()
        self.filename = filename
        self.running = True
        self.daemon = True  
        self.values = []
        self.minutes = minutes * 60
        self.secondperfloat = secondperfloat



    def run(self):
        #Open csv and set it so it flushes the buffer every time a row is written
        with open(self.filename, 'w', newline='',buffering=True) as csvfile:

            #Set the writter variable and set the column names
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Timestamp', 'Float Generated'])

            #Generate a random variable and write it in the csv file
            while self.running:
                random_float = random.uniform(25.0, 45.0)
                self.values.append(random_float)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                csvwriter.writerow([timestamp, random_float])
                time.sleep(self.secondperfloat)



    def stop(self):
        self.running = False