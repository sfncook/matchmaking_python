import os
import json
from pprint import pprint
import random
import numpy as np

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


    def add_review(self, consumer_uuid:str, product_uuid:str, review_quantitative:int):
        consumer = self.get_consumer_by_uuid(consumer_uuid)
        product = self.get_product_by_uuid(product_uuid)
        consumer_point = consumer['point']
        product_point = product['point']
        new_consumer_point, new_product_point = self.move_points_by_distance(consumer_point, product_point, review_quantitative)
        print("CONSUMER")
        pprint(consumer_point)
        pprint(new_consumer_point)
        print("\nPRODUCT")
        pprint(product_point)
        pprint(new_product_point)


    def get_consumer_by_uuid(self, consumer_uuid: str):
        return next((md for md in self.consumers_data if md["uuid"] == consumer_uuid), None)

    def get_product_by_uuid(self, product_uuid: str):
        return next((md for md in self.products_data if md["uuid"] == product_uuid), None)
        

    def move_points_by_distance(self, consumer_point, product_point, distance=1.0):
        # Convert lists to numpy arrays for easier calculations
        v1 = np.array(consumer_point)
        v2 = np.array(product_point)
        
        # Calculate the difference vector
        diff_vector = v2 - v1
        
        # Normalize the difference vector
        norm_diff_vector = diff_vector / np.linalg.norm(diff_vector)
        
        # Move each point away from the other by the specified distance
        new_v1 = v1 - norm_diff_vector * -distance
        new_v2 = v2 + norm_diff_vector * -distance
        
        new_consumer_point = new_v1.tolist()
        new_product_point = new_v2.tolist()

        return new_consumer_point, new_product_point


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

