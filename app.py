from flask import Flask
from flask_cors import CORS
from api.endpoints import create_api_blueprint
from storage.flatfile_vector_store import FlatFileVectorStore
from storage.consumer_store import ConsumerStore
import os

app = Flask(__name__)
CORS(app)

DIMENSIONS = 12

vector_store = FlatFileVectorStore(DIMENSIONS)
consumer_store = ConsumerStore(DIMENSIONS)

app.register_blueprint(create_api_blueprint(vector_store, consumer_store))

def initialize_app():
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        vector_store.initialize()
        consumer_store.initialize()

if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)
