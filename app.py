from flask import Flask
from flask_cors import CORS
from api.endpoints import create_api_blueprint
from storage.flatfile_vector_store import FlatFileVectorStore
from storage.consumer_store import ConsumerStore
from storage.product_store import ProductStore
import os

app = Flask(__name__)
CORS(app)

DIMENSIONS = 12
MIN_VECTOR_VALUE = -10
MAX_VECTOR_VALUE = 10

vector_store = FlatFileVectorStore(DIMENSIONS)
consumer_store = ConsumerStore(DIMENSIONS, MIN_VECTOR_VALUE, MAX_VECTOR_VALUE)
product_store = ProductStore(DIMENSIONS, MIN_VECTOR_VALUE, MAX_VECTOR_VALUE)

app.register_blueprint(create_api_blueprint(vector_store, consumer_store, product_store))

@app.before_first_request
def initialize_app():
    # Initialize stores only once
    vector_store.initialize()
    consumer_store.initialize()
    product_store.initialize()

if __name__ == '__main__':
    app.run(debug=True)  # Keep debug=True for development; consider setting to False in production
