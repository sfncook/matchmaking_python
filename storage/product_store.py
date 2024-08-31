import os
import json
from pprint import pprint
import random

PRODUCT_DB_FILE = 'products_db_004.json'

class ProductStore:
    def __init__(self, dimensions, min_vector_value, max_vector_value):
        self.dimensions = dimensions
        self.min_vector_value = min_vector_value
        self.max_vector_value = max_vector_value
        self.product_db_file = os.path.join("data", PRODUCT_DB_FILE)
        self.products_data = []

    def initialize(self):
        self.load_db_file()

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
        if os.path.exists(self.product_db_file):
            with open(self.product_db_file, 'r') as f:
                self.products_data = json.load(f)
        else:
            print(f"Product file does not exist {self.product_db_file}")

    def save_db_file(self):
        with open(self.product_db_file, 'w') as f:
            json.dump(self.products_data, f, indent=4)