import random
import time

import pytest

from src.utilities import utilities
from src.helpers.APIHelper import APIHelper

pytestmark = [pytest.mark.api, pytest.mark.regression]

logger = utilities.custom_logger()


def test_update_existing_pet():
    api_helper = APIHelper()
    logger.info("Get list of all pets with status available")
    available_pets_json = api_helper.get_pets_by_status("available", 200)

    logger.info("Select random pet from retrieved list")
    random_pet = random.choice([pet for pet in available_pets_json])
    logger.info(f"Selected random pet: {random_pet}")

    random_pet["name"] = api_helper.generate_random_date("pet_name")
    random_pet["status"] = api_helper.generate_random_date("pet_status")
    logger.info(f"Update retrieved pet data with random name: {random_pet['name']}, status: {random_pet['status']}")
    api_helper.post_update_pet_by_id(random_pet["id"], random_pet["name"], random_pet["status"], 200)

    pet_json_after_update = api_helper.get_pet_by_id(random_pet["id"], 200)
    logger.warning("Check pet data updated correctly")
    assert pet_json_after_update == random_pet


def test_place_order():
    api_helper = APIHelper()
    new_pet_json_payload = api_helper.generate_random_date("pet_payload")
    logger.info(f"Add new pet with random data: {new_pet_json_payload}")
    pet_json_after_add = api_helper.post_add_pet(new_pet_json_payload, 200)

    new_order_json_payload = api_helper.generate_random_date("order_payload", pet_id=pet_json_after_add["id"])
    logger.info(f"Place new order with the created pet id and random data: {new_order_json_payload}")
    place_order_json_response = api_helper.post_place_order(new_order_json_payload, 200)

    placed_order_json = api_helper.get_order_by_id(place_order_json_response["id"], 200)
    logger.warning("Check order is placed correctly")
    assert placed_order_json == place_order_json_response


def test_update_inventory():
    api_helper = APIHelper()
    logger.info("Get list of all pets with status available")
    available_pets_json = api_helper.get_pets_by_status("available", 200)

    logger.info("Select random pet from retrieved list")
    random_pet = random.choice([pet for pet in available_pets_json])
    logger.info(f"Selected random pet: {random_pet}")

    inventory_before_update = api_helper.get_inventory(200)
    logger.info(f"Inventory data before update: {inventory_before_update}")

    random_pet["status"] = "pending"
    logger.info("Update retrieved pet data with status: pending")
    api_helper.post_update_pet_by_id(random_pet["id"], random_pet["name"], random_pet["status"], 200)

    # Wait for the inventory to be updated
    time.sleep(1)
    inventory_after_update = api_helper.get_inventory(200)
    logger.info(f"Inventory data before update: {inventory_after_update}")
    logger.warning("Check inventory data updated correctly")
    assert inventory_before_update["available"] - inventory_after_update["available"] == 1
    assert inventory_before_update["pending"] - inventory_after_update["pending"] == -1


def test_delete_existing_pet():
    api_helper = APIHelper()
    new_pet_json_payload = api_helper.generate_random_date("pet_payload")
    logger.info(f"Add new pet with random data: {new_pet_json_payload}")
    pet_json_after_add = api_helper.post_add_pet(new_pet_json_payload, 200)

    logger.info("Read added pet data")
    added_pet_json = api_helper.get_pet_by_id(pet_json_after_add["id"], 200)

    logger.info(f"Delete added pet by id: {added_pet_json['id']}")
    api_helper.delete_pet_by_id(added_pet_json["id"], 200)

    logger.info("Try reading deleted pet data by id")
    get_deleted_pet_json_response = api_helper.get_pet_by_id(pet_json_after_add["id"], 404)

    logger.warning(f"Check response message is: Pet not found")
    assert get_deleted_pet_json_response["type"] == "error"
    assert get_deleted_pet_json_response["message"] == "Pet not found"
