import requests
import json


def find(district_code=None, date=None):
    covaxin_filter = list()
    covishield_filter = list()

    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(district_code, date)
    headers = {"Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36",
               "Accept-Language": "en_US"}
    response = requests.get(url=url, headers=headers)

    if not response.content:
        return

    response = json.loads(response.content.decode("utf-8", "ignore"))
    response = response["sessions"]

    for r in response:
        r = dict(r)
        if r["vaccine"] == "COVAXIN" and r["available_capacity"] > 0:
            covaxin_filter.append(r)
        if r["vaccine"] == "COVISHIELD" and r["available_capacity"] > 0:
            covishield_filter.append(r)

    return {"covaxin": covaxin_filter,
            "covishield": covishield_filter}
