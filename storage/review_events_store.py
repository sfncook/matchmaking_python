import os
import json
from datetime import datetime

REVIEW_EVENTS_DB_FILE = 'random_points/review_events_db_006.json'

class Review_Events_Store:
    def __init__(self):
        self.review_events_db_file = os.path.join("data", REVIEW_EVENTS_DB_FILE)
        self.review_events_data = []

    def initialize(self):
        self.load_db_file()

    def add_new_review_event(self, uuid: str, consumer_uuid:str, product_uuid:str,review_quantitative:int):
        new_review_event_datem = {
            "uuid": uuid,
            "consumer_uuid": consumer_uuid,
            "product_uuid": product_uuid,
            "review_quantitative": review_quantitative,
            "timestamp": datetime.now().isoformat()
        }
        self.review_events_data.append(new_review_event_datem)
        self.save_db_file()

    def get_all_review_events(self):
        return self.review_events_data

    def get_count_review_events_for_consumer(self, consumer_uuid: str) -> int:
        return sum(1 for event in self.review_events_data if event.get("consumer_uuid") == consumer_uuid)

    def get_count_review_events_for_product(self, product_uuid: str) -> int:
        return sum(1 for event in self.review_events_data if event.get("product_uuid") == product_uuid)

    def load_db_file(self):
        if os.path.exists(self.review_events_db_file):
            with open(self.review_events_db_file, 'r') as f:
                self.review_events_data = json.load(f)
        else:
            print(f"Review Events file does not exist {self.review_events_db_file}")

    def save_db_file(self):
        with open(self.review_events_db_file, 'w') as f:
            json.dump(self.review_events_data, f, indent=4)

