from flask import Blueprint, request, jsonify
import numpy as np
import random
import uuid
from pprint import pprint
import pickle
import json
import os

api = Blueprint('api', __name__)

def create_api_blueprint(vector_store):

    @api.route('/hello', methods=['GET'])
    def hello_world():
        return jsonify({
            "consumers": vector_store.get_all_consumers(),
            "products": vector_store.get_all_products(),
        }), 200

    @api.route('/consumers', methods=['POST'])
    def add_random_consumer():
        consumer_uuid = str(uuid.uuid4())
        vector_store.add_new_consumer_random(consumer_uuid)
        return jsonify({"uuid":consumer_uuid}), 201

    @api.route('/consumers', methods=['GET'])
    def get_all_consumers():
        return jsonify({"consumers":vector_store.get_all_consumers()}), 200

    @api.route('/products', methods=['POST'])
    def add_random_product():
        product_uuid = str(uuid.uuid4())
        vector_store.add_new_product_random(product_uuid)
        return jsonify({"uuid":product_uuid}), 201

    @api.route('/products/<string:product_uuid>', methods=['GET'])
    def get_single_product(product_uuid):
        product = vector_store.get_product_by_uuid(product_uuid)
        if product is None:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product), 200

    @api.route('/consumers/<string:consumer_uuid>', methods=['GET'])
    def get_single_consumer(consumer_uuid):
        product = vector_store.get_consumer_by_uuid(consumer_uuid)
        if product is None:
            return jsonify({'error': 'Consumer not found'}), 404
        return jsonify(product), 200

    return api
