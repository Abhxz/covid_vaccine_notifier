from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from configparser import ConfigParser

configparser = ConfigParser()
configparser.read("config.cfg")

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

pincode = configparser.get("data", "pincode")
vaccine_name = configparser.get("data", "vaccine_name").split(",")
district_name = configparser.get("data", "district_name")
account_sid = configparser.get("data", "account_sid")
auth_token = configparser.get("data", "auth_token")
from_ = configparser.get("data", "from_")
to = configparser.get("data", "to")