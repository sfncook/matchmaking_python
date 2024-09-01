import os
import json
from pprint import pprint
import random

CONSUMER_DB_FILE = 'consumers_db_004.json'
PRODUCT_DB_FILE = 'products_db_004.json'

DIMENSIONS = 12
MIN_VECTOR_VALUE = -10
MAX_VECTOR_VALUE = 10

class FlatFile_LatLonSpherical_VectorStore:
    def __init__(self):
        self.dimensions = DIMENSIONS
        self.min_vector_value = MIN_VECTOR_VALUE
        self.max_vector_value = MAX_VECTOR_VALUE
        self.consumer_db_file = os.path.join("data", CONSUMER_DB_FILE)
        self.product_db_file = os.path.join("data", PRODUCT_DB_FILE)
        self.products_data = []
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

    def add_new_product_random(self, uuid: str):
        new_product_datem = {
            "uuid": uuid,
            "point": [random.uniform(self.min_vector_value, self.max_vector_value) for _ in range(self.dimensions)]
        }
        self.products_data.append(new_product_datem)
        self.save_db_file()
        pprint(new_product_datem)

    def get_all_products(self):
        return self.products_data

    def load_db_file(self):
        if os.path.exists(self.consumer_db_file):
            with open(self.consumer_db_file, 'r') as f:
                self.consumers_data = json.load(f)
        else:
            print(f"Consumer file does not exist {self.consumer_db_file}")

        if os.path.exists(self.product_db_file):
            with open(self.product_db_file, 'r') as f:
                self.products_data = json.load(f)
        else:
            print(f"Product file does not exist {self.product_db_file}")

    def save_db_file(self):
        with open(self.consumer_db_file, 'w') as f:
            json.dump(self.consumers_data, f, indent=4)
        with open(self.product_db_file, 'w') as f:
            json.dump(self.products_data, f, indent=4)

