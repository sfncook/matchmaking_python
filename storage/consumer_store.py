import os
import json
from pprint import pprint
import random

CONSUMER_DB_FILE = 'consumer_db_004.json'
MIN_VECTOR_VALUE = -10
MAX_VECTOR_VALUE = 10

class ConsumerStore:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.consumer_db_file = os.path.join("data", CONSUMER_DB_FILE)
        self.consumers_data = []

    def initialize(self):
        self.load_db_file()
        print("Loaded consumers:")
        pprint(self.consumers_data)

    def add_new_consumer_random(self, uuid: str):
        new_consumer_datem = {
            "uuid": uuid,
            "point": [random.uniform(MIN_VECTOR_VALUE, MAX_VECTOR_VALUE) for _ in range(self.dimensions)]
        }
        self.consumers_data.append(new_consumer_datem)
        self.save_db_file()
        pprint(new_consumer_datem)

    def load_db_file(self):
        if os.path.exists(self.consumer_db_file):
            with open(self.consumer_db_file, 'r') as f:
                self.consumers_data = json.load(f)

    def save_db_file(self):
        with open(self.consumer_db_file, 'w') as f:
            json.dump(self.consumers_data, f, indent=4)