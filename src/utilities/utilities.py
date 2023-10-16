import json
import logging
import os
from configparser import ConfigParser
from pathlib import Path


def custom_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    parent_path = Path(os.path.dirname(os.path.abspath(__file__))).parent
    log_file_path = os.path.join(parent_path, "results/automation_logs.log")
    file_handler = logging.FileHandler(log_file_path, mode="w")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def read_env_variables(key):
    return os.getenv(key)


def read_configs(section, option):
    config = ConfigParser()
    configs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs"))
    config_file_path = configs_path + "/config.ini"
    config.read(config_file_path)
    return config.get(section, option)


def read_web_login_test_data():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/test_data"))
    web_login_file_path = data_path + "/web_login_data.json"
    data = json.load(open(web_login_file_path))
    return data


def read_get_pet_schema():
    return read_schema_json_file("get_pet_schema")


def read_get_pets_schema():
    return read_schema_json_file("get_pets_schema")


def read_post_pet_schema():
    return read_schema_json_file("post_pet_schema")


def read_error_message_schema():
    return read_schema_json_file("error_response_schema")


def read_get_order_schema():
    return read_schema_json_file("get_order_schema")


def read_get_inventory_schema():
    return read_schema_json_file("get_inventory_schema")


def read_schema_json_file(file):
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/schemas"))
    web_login_file_path = data_path + "/" + file + ".json"
    data = json.load(open(web_login_file_path))
    return data
