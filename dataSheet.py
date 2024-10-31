import datetime
import os

import requests


class DataSheet:

    def __init__(self):
        self.sheet_link = os.getenv('SHEET_LINK')
        self.data = None

    def read_data(self):
        response = requests.get(self.sheet_link)
        response.raise_for_status()
        self.data = response.json()

        return response.json()


    def write_data(self, data):
        for i in data:
            created_data = {
                "sheet1": {
                    "href": i["href"],
                    "title": i["job_title"],
                    "company": i["company"],
                    "time": datetime.datetime.now().strftime("%d/%m/%Y")
                }
            }

            response = requests.post(self.sheet_link, json=created_data)
            response.raise_for_status()
        print("data written to GSheets")

    def return_hrefs(self):
        return [i['href'] for i in self.read_data()['sheet1']]