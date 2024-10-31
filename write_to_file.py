import datetime
import os

import pandas as pd


class WriteToFile:

    def __init__(self, file_name):
        self.file_name = file_name
        # self.file_name = "data.csv"
        if not os.path.exists(self.file_name):
            # os.makedirs(self.file_name.split("/")[0])
            self.create_file()

    def create_file(self):
        col_names = ["Href", "Title", "Company", "Time"]
        new_table = pd.DataFrame(columns=col_names)
        new_table.to_csv(self.file_name,sep="|")


    def write_data_to_file(self, data):
        hrefs = [ i['href'] for i in data]
        companies = [ i['company'] for i in data]
        titles = [ i['job_title'] for i in data]
        time = [datetime.datetime.now().strftime("%d/%m/%Y") for i in data]

        created_data = {
            "Href":hrefs,
            "Title":titles,
            "Company": companies,
            "Time":time
        }
        pd.DataFrame.from_dict(created_data).to_csv(self.file_name,mode="a",sep="|",header=False)
        print("Written to the file successfully")


    def read_file_return_hrefs(self):
        resource= pd.read_csv(self.file_name,sep="|",usecols=["Href"])

        return [ i for i in resource.to_dict()["Href"].values()]


