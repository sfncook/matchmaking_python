import os
import json
from pprint import pprint
import random

CONSUMER_DB_FILE = 'consumers_db_004.json'

class ConsumerStore:
    def __init__(self, dimensions, min_vector_value, max_vector_value):
        self.dimensions = dimensions
        self.min_vector_value = min_vector_value
        self.max_vector_value = max_vector_value
        self.consumer_db_file = os.path.join("data", CONSUMER_DB_FILE)
        self.consumers_data = []

    def initialize(self):
        self.load_db_file()

    def add_new_consumer_random(self, uuid: str):
        new_consumer_datem = {
            "uuid": uuid,
            "point": [random.uniform(self.min_vector_value, self.max_vector_value) for _ in range(self.dimensions)]
        }
        self.consumers_data.append(new_consumer_datem)
        self.save_db_file()
        pprint(new_consumer_datem)

    def get_all_consumers(self):
        pprint(self.consumers_data)
        return self.consumers_data

    def load_db_file(self):
        if os.path.exists(self.consumer_db_file):
            with open(self.consumer_db_file, 'r') as f:
                self.consumers_data = json.load(f)
        else:
            print(f"Consumer file does not exist {self.consumer_db_file}")

    def save_db_file(self):
        with open(self.consumer_db_file, 'w') as f:
            json.dump(self.consumers_data, f, indent=4)
