import os
import json
from pprint import pprint
import random
import numpy as np

CONSUMER_DB_FILE = 'consumers_db_005.json'
PRODUCT_DB_FILE = 'products_db_005.json'

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


    def get_distance_between(self, consumer_uuid:str, product_uuid:str):
        consumer = self.get_consumer_by_uuid(consumer_uuid)
        product = self.get_product_by_uuid(product_uuid)
        consumer_point = consumer['point']
        product_point = product['point']

        # Convert lists to numpy arrays for easier calculations
        v1 = np.array(consumer_point)
        v2 = np.array(product_point)
        
        # Calculate the Euclidean distance
        distance = np.linalg.norm(v2 - v1)
        
        return distance

    def get_max_distance(self):
        # The distance between MIN_VECTOR_VALUE and MAX_VECTOR_VALUE
        max_diff = MAX_VECTOR_VALUE - MIN_VECTOR_VALUE
        
        # The maximum distance is achieved when points are opposite in all dimensions
        max_distance = np.sqrt(DIMENSIONS * (max_diff / 2) ** 2)
        
        return max_distance

    def add_review(self, consumer_uuid:str, product_uuid:str, review_quantitative:int):
        consumer = self.get_consumer_by_uuid(consumer_uuid)
        product = self.get_product_by_uuid(product_uuid)
        consumer_point = consumer['point']
        product_point = product['point']
        new_consumer_point, new_product_point = self.move_points_by_distance(consumer_point, product_point, review_quantitative)
        self.update_datem_point_by_uuid(self.consumers_data, consumer_uuid, new_consumer_point)
        self.update_datem_point_by_uuid(self.products_data, product_uuid, new_product_point)
        self.save_db_file()

    def update_datem_point_by_uuid(self, data, uuid, new_point):
        for datem in data:
            if datem['uuid'] == uuid:
                datem['point'] = new_point

    def get_consumer_by_uuid(self, consumer_uuid: str):
        return next((md for md in self.consumers_data if md["uuid"] == consumer_uuid), None)

    def get_product_by_uuid(self, product_uuid: str):
        return next((md for md in self.products_data if md["uuid"] == product_uuid), None)
    
    def find_nearest_products(self, consumer_uuid: str, n: int):
        # Ensure n is an integer
        if not isinstance(n, int):
            print(f"Type of n: {type(n)}")
            print(f"Value of n: {n}")
            print(f"Number of distances available: {len(distances)}")

            raise ValueError(f"The number of nearest products 'n' must be an integer. {n}")
        
        consumer = self.get_consumer_by_uuid(consumer_uuid)
        consumer_point = consumer['point']
        consumer_point_np = np.array(consumer_point)
        
        distances = []
        for product in self.products_data:
            product_uuid = product['uuid']  # Keep product_uuid as a string
            product_point = np.array(product['point'])
            distance = np.linalg.norm(product_point - consumer_point_np)
            distances.append((distance, product_uuid))
        
        distances.sort(key=lambda x: x[0])
        
        # Ensure distances contains enough elements and n is within bounds
        if n > len(distances):
            raise ValueError(f"Requested number of nearest products 'n' ({n}) exceeds available products ({len(distances)}).")
        
        nearest_n_product_uuids = [product_uuid for _, product_uuid in distances[:n]]
        
        return nearest_n_product_uuids

    def get_all_distances(self, consumer_uuid):
        consumer = self.get_consumer_by_uuid(consumer_uuid)
        consumer_point = consumer['point']
        consumer_point_np = np.array(consumer_point)
        distances = []
        for product in self.products_data:
            product_point_np = np.array(product['point'])
            distance = np.linalg.norm(product_point_np - consumer_point_np)
            distances.append((distance, product['uuid']))
        distances.sort(key=lambda x: x[0])
        sorted_products = [{"uuid": uuid, "distance": distance} for distance, uuid in distances]
        return sorted_products

    def move_points_by_distance(self, consumer_point, product_point, review_quantitative=1.0):
        # Convert review_quantitative to distance
        distance = review_quantitative / 5

        # Convert lists to numpy arrays for easier calculations
        v1 = np.array(consumer_point)
        v2 = np.array(product_point)
        
        # Calculate the difference vector
        diff_vector = v2 - v1
        
        # Handle the case where any dimension in the diff_vector is 0
        zero_mask = diff_vector == 0
        if np.any(zero_mask):
            # Replace zeros with small random values
            diff_vector[zero_mask] = np.random.uniform(-0.0001, 0.0001, size=np.sum(zero_mask))
        
        # Normalize the difference vector
        norm_diff_vector = diff_vector / np.linalg.norm(diff_vector)
        
        # Move each point away from the other by the specified distance
        new_v1 = v1 - norm_diff_vector * -distance
        new_v2 = v2 + norm_diff_vector * -distance
        
        # Wrap around dimensions that are out of bounds
        new_v1 = self.wrap_vector(new_v1)
        new_v2 = self.wrap_vector(new_v2)
        
        new_consumer_point = new_v1.tolist()
        new_product_point = new_v2.tolist()

        return new_consumer_point, new_product_point

    def wrap_vector(self, vector):
        # Wrap each dimension within the MIN_VECTOR_VALUE and MAX_VECTOR_VALUE range
        wrapped_vector = np.where(vector < MIN_VECTOR_VALUE, 
                                  MAX_VECTOR_VALUE - (MIN_VECTOR_VALUE - vector) % (MAX_VECTOR_VALUE - MIN_VECTOR_VALUE), 
                                  vector)
        wrapped_vector = np.where(wrapped_vector > MAX_VECTOR_VALUE, 
                                  MIN_VECTOR_VALUE + (wrapped_vector - MAX_VECTOR_VALUE) % (MAX_VECTOR_VALUE - MIN_VECTOR_VALUE), 
                                  wrapped_vector)
        return wrapped_vector

    def interpolate_prediction(self, distance):
        """
        Interpolate prediction value based on distance using linear interpolation
        between MIN_DISTANCE and MAX_DISTANCE.
        """
        MIN_DISTANCE = 0.4
        MAX_DISTANCE = 34.0
        MIN_PREDICTION = 10
        MAX_PREDICTION = -10
        if distance <= MIN_DISTANCE:
            return MIN_PREDICTION
        elif distance >= MAX_DISTANCE:
            return MAX_PREDICTION
        else:
            # Linear interpolation
            normalized_distance = (distance - MIN_DISTANCE) / (MAX_DISTANCE - MIN_DISTANCE)
            return MAX_PREDICTION + (MIN_PREDICTION - MAX_PREDICTION) * (1 - normalized_distance)


    def get_predictions(self, consumer_uuid, product_uuids):
        consumer = self.get_consumer_by_uuid(consumer_uuid)
        consumer_point = consumer['point']
        consumer_point_np = np.array(consumer_point)
        predictions = []
        for product_uuid in product_uuids:
            product = self.get_product_by_uuid(product_uuid)
            product_point = product['point']
            product_point_np = np.array(product_point)
            
            # Calculate the distance between consumer and product points
            distance = np.linalg.norm(product_point_np - consumer_point_np)
            prediction_value = self.interpolate_prediction(distance)
            predictions.append({"uuid": product_uuid, "distance": distance, "prediction": prediction_value})
        
        return predictions


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






