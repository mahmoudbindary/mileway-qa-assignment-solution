import random
from datetime import datetime

import requests
from faker import Faker
from faker.providers import internet
from jsonschema.validators import validate
from requests.auth import HTTPBasicAuth

from src.utilities import utilities


# Helper class for API tests
class APIHelper:
    def __init__(self):
        # Urls
        self.api_base_url = utilities.read_configs("api", "api_base_url")
        self.pet_url = f"{self.api_base_url}/pet"
        self.pet_find_by_status_url = f"{self.api_base_url}/pet/findByStatus"
        self.order_url = f"{self.api_base_url}/store/order"
        self.inventory_url = f"{self.api_base_url}/store/inventory"

        # Values
        self.api_key = utilities.read_env_variables("api_key")
        self.pet_statuses = ["available", "pending", "sold"]
        self.order_statuses = ["placed", "approved", "delivered"]
        self.expected_content_type = "application/json"

        # Library to generate random data
        self.fake = Faker()
        self.fake.add_provider(internet)

    # HTTPS Request Methods
    def get_pets_by_status(self, status, expected_status_code):
        params = {"status": status}
        response = requests.get(url=self.pet_find_by_status_url, params=params)

        # Check expected status code, content-type header and json schema for each request
        self.assert_status_code(response, expected_status_code)
        self.assert_content_type(response, self.expected_content_type)
        self.assert_schema(response, utilities.read_get_pets_schema())
        return response.json()

    def get_inventory(self, expected_status_code):
        response = requests.get(url=self.inventory_url)
        self.assert_status_code(response, expected_status_code)
        self.assert_content_type(response, self.expected_content_type)
        self.assert_schema(response, utilities.read_get_inventory_schema())
        return response.json()

    def get_pet_by_id(self, pet_id, expected_status_code):
        response = requests.get(url=self.pet_url + f"/{pet_id}")
        self.assert_status_code(response, expected_status_code)
        self.assert_content_type(response, self.expected_content_type)
        if "id" in response.json():
            self.assert_schema(response, utilities.read_get_pet_schema())
        else:
            self.assert_schema(response, utilities.read_error_message_schema())
        return response.json()

    def get_order_by_id(self, order_id, expected_status_code):
        response = requests.get(url=self.order_url + f"/{order_id}")
        self.assert_status_code(response, expected_status_code)
        self.assert_content_type(response, self.expected_content_type)
        # Expected json schema changes if ID is correct or not
        if "id" in response.json():
            self.assert_schema(response, utilities.read_get_order_schema())
        else:
            self.assert_schema(response, utilities.read_error_message_schema())
        return response.json()

    def post_update_pet_by_id(self, pet_id, name, status, expected_status_code):
        pet_data = {"name": name, "status": status}
        response = requests.post(url=self.pet_url + f"/{pet_id}", data=pet_data)
        self.assert_status_code(response, expected_status_code)
        self.assert_content_type(response, self.expected_content_type)
        if "id" in response.json():
            self.assert_schema(response, utilities.read_post_pet_schema())
        else:
            self.assert_schema(response, utilities.read_error_message_schema())

    def post_add_pet(self, json_payload, expected_status_code):
        response = requests.post(url=self.pet_url, json=json_payload)
        self.assert_status_code(response, expected_status_code)
        self.assert_content_type(response, self.expected_content_type)
        self.assert_schema(response, utilities.read_get_pet_schema())
        return response.json()

    def post_place_order(self, json_payload, expected_status_code):
        response = requests.post(url=self.order_url, json=json_payload)
        self.assert_status_code(response, expected_status_code)
        self.assert_content_type(response, self.expected_content_type)
        self.assert_schema(response, utilities.read_get_order_schema())
        return response.json()

    def delete_pet_by_id(self, pet_id, expected_status_code):
        api_auth = HTTPBasicAuth("apikey", self.api_key)
        response = requests.delete(url=self.pet_url + f"/{pet_id}", auth=api_auth)
        self.assert_status_code(response, expected_status_code)
        self.assert_content_type(response, self.expected_content_type)

    # General Methods
    @staticmethod
    def assert_status_code(response, expected_status_code):
        assert response.status_code == expected_status_code

    @staticmethod
    def assert_content_type(response, expected_content_type):
        assert response.headers["content-type"] == expected_content_type

    @staticmethod
    def assert_schema(response, schema):
        validate(instance=response.json(), schema=schema)

    def generate_random_date(self, data_type, **kwargs):
        if data_type == "pet_name":
            return self.fake.first_name()
        elif data_type == "pet_status":
            return random.choice([status for status in self.pet_statuses])
        elif data_type == "pet_payload":
            return {"name": self.fake.first_name(),
                    "photoUrls": [self.fake.image_url()],
                    "status": "available"}
        elif data_type == "order_payload":
            return {"petId": kwargs["pet_id"],
                    "quantity": random.randint(1, 5),
                    "shipDate": datetime.now().isoformat(),
                    "status": random.choice([status for status in self.order_statuses]),
                    "complete": random.choice([True, False])}
        else:
            return ""
