import secrets
import time
from flask import Flask

from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client

import data
import findByDistrict
import findByPin
import regionData

vaccine = Flask(__name__)

scheduler = BackgroundScheduler(executors=data.executors, job_defaults=data.job_defaults)


@vaccine.route("/initiate", methods=["GET"])
def initial_trigger():
    initiate_program()


def date_generator():
    today = str(time.strftime("%d-%m-%Y"))
    day = int(today[0:2])
    month = int(today[3:5])
    year = int(today[6:10])
    dates = list()
    for _ in range(0, 7):
        dates.append("{}-{}-{}".format(day, month, year))
        if day + 1 <= 31:
            day += 1
        elif month < 12:
            day = 1
            month += 1

    return dates


def call_find_by_pin():
    pincode = data.pincode
    vaccine_name = data.vaccine_name
    final_update = {key: [] for key in vaccine_name}
    dates = date_generator()
    for date in dates:
        result = findByPin.find(date=date, pincode=pincode)
        if result["covaxin"]:
            final_update["covaxin"].append(result["covaxin"])
        if result["covishield"]:
            final_update["covishield"].append(result["covishield"])

    if final_update['covaxin']:
        print("\nSlots for COVAXIN is available now. Please book before it exhaust")
    else:
        print("\nNo slots for COVAXIN for next 7 days")

    if final_update['covishield']:
        print("\nSlots for COVISHIELD is available now. Please Book before it exhaust")
    else:
        print("\nNo slots for COVISHIELD for next 7 days")

    processing_result(final_update)


def call_find_by_district():
    district_name = data.district_name
    district_code = regionData.district_dictionary[district_name]
    vaccine_name = data.vaccine_name
    final_update = {key: [] for key in vaccine_name}
    dates = date_generator()
    for date in dates:
        result = findByDistrict.find(district_code=district_code, date=date)

        if result["covaxin"]:
            final_update["covaxin"].append(result["covaxin"])
        if result["covishield"]:
            final_update["covishield"].append(result["covishield"])

    if final_update['covaxin']:
        print("\nSlots for COVAXIN is available now. Please book before it exhaust")
    else:
        print("\nNo slots for COVAXIN for next 7 days")

    if final_update['covishield']:
        print("\nSlots for COVISHIELD is available now. Please Book before it exhaust")
    else:
        print("\nNo slots for COVISHIELD for next 7 days")

    processing_result(final_update)


def processing_result(final_update):
    covaxincenter = extract_covaxin_centers(final_update["covaxin"])
    covishieldcenter = extract_covishield_centers(final_update['covishield'])

    if covaxincenter:
        covaxinmsgforuser = "Covaxin Slots are available in following centers {}. Please book your slot before it " \
                            "exhaust.".format(covaxincenter)
    else:
        covaxinmsgforuser = "No slots available for COVAXIN"

    if covishieldcenter:
        covishieldmsgforuser = "Covishield Slots are available in following centers {}. Please book your slot before " \
                               "it exhaust.".format(covishieldcenter)
    else:
        covishieldmsgforuser = "No clots available for COVISHIELD"

    user_message = "\n" + covaxinmsgforuser + "\n" + covishieldmsgforuser + "\n"

    alert_user(user_message)


def extract_covaxin_centers(result):
    covaxin_center = ""
    number = 1
    for d in result:
        for covaxin in d:
            if covaxin["name"]:
                covaxin_center += str(number) + " " + covaxin["name"] + " "

    return covaxin_center


def extract_covishield_centers(result):
    covishield_center = ""
    number = 1
    for d in result:
        for covishield in d:
            if covishield["name"]:
                covishield_center += str(number) + " " + covishield["name"] + " "

    return covishield_center


def alert_user(message):
    client = Client(data.account_sid, data.auth_token)

    message = client.messages.create(body=message,
                                     from_=data.from_,
                                     to=data.to)

    print(message.sid)


def initiate_program():
    print("Program is started and will called in 1 minute")
    scheduler.add_job(id="callByDistrict", func=call_find_by_district, trigger="interval", minutes=1)
    scheduler.start()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # call_find_by_pin()
    vaccine.secret_key = secrets.token_urlsafe(10)
    initiate_program()
    vaccine.run(host="0.0.0.0", port=5080, threaded=True)
