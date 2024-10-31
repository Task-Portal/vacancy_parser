import os
from pprint import pprint


from dotenv import load_dotenv
import requests

from VacancyParser import VacancyParser
from VacancyParserSoup import VacancyPSoup
from notification_manager import NotificationManager
from write_to_file import WriteToFile

load_dotenv()

# wf = WriteToFile()

# region Wrong Words
wrong_words = ["senior", "wordpress", "ios",  "ментор",  "designer", "ruby", "unity",
                             "сіньйор", "flutter",  "golang",
                            "delphi", "rust", "vue", "1c", "1С", "dart/flutter", "manager", "vba",
                            "5+", "php/symfony", "php-програміст", "1c-розробник", "java/android",
                            "(Wordpress)",
                            "dev", "інженер-програміст мікроконтролерів", "aдміністратор", 
                            "pl/sql", "erlang", "начальник", "1с:підприємство", "sql-розробник", "(vue.js,",
                            "kotlin/java","warcraft",
                            "vue.js", "senior/middle", "embedded", "middle/senior", "native)", "vue.js)",
                            "php/golang",
                            "game", "account", "qa", "tree.js", "lead", "викладач", "perl",
                            "unity3d", "(laravel,", "php-developer", "wordpress-розробник", "java-розробник",
                            ".net/blazor", "kotlin", "native", "opencart",  "мобильных", "tree.js",
                            "(middle/senior)",
                            "laravel/vue.js", "1С", "wordpress-developer", "golang)", "vuejs", "wordpress/php",
                            "drupal", "odoo", "swift-розробник",
                            "(delphi)", "umbraco", "(ios/android)", "magento", "unreal", "drupal", "drupal-программист",
                            "scala","symfony", "lead/senior","(rust)", "(/ibp)","acquisition","creatio","java-разработчик",
                            "codeless","c#",".net", "c++", "php", "android", "java"
                            ]
# endregion

# region Companies
companies = ["step", "globallogic", "luxoft", "evoplay", "genesis","uvocorp", "tuteat","Клименко"]
# endregion


# region Robota Ua
# 500
print("rabota.ua")
wf= WriteToFile(file_name="data/robota_ua.csv")
p = VacancyParser(site="https://rabota.ua/ua/zapros/programmer/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0",wrong_words=wrong_words, companies=companies,
                  headless=False)


p.parser_robota_ua(wf.read_file_return_hrefs())

if (len(p.jobs)) > 0:
    nm = NotificationManager()
    nm.send_email(p.jobs, [os.getenv('EMAIL_TO')])
    wf.write_data_to_file(p.jobs)
# endregion


#region Work Ua
# work.ua Done
print("works.ua")
wf= WriteToFile(file_name="data/work_ua.csv")
p = VacancyParser(site="https://www.work.ua/jobs-it-programmer/?advs=1", wrong_words=wrong_words, companies=companies)

p.parser_work_ua(wf.read_file_return_hrefs())

if (len(p.jobs)) > 0:
    nm = NotificationManager()
    nm.send_email(p.jobs, [os.getenv('EMAIL_TO')])
    wf.write_data_to_file(p.jobs)
# endregion


# region Olx.ua

print("Olx Ua")
wf= WriteToFile(file_name="data/olx_ua.csv")
link = "https://www.olx.ua/d/uk/rabota/it-telekom-kompyutery/?currency=UAH&search%5Bfilter_enum_job_type%5D%5B0%5D=remote"
p = VacancyPSoup(link=link,
                 wrong_words=wrong_words, companies=companies, hrefs=wf.read_file_return_hrefs())
p.get_data_olx_ua()

if (len(p.jobs)) > 0:
    nm = NotificationManager()
    nm.send_email(p.jobs, [os.getenv('EMAIL_TO')])
    wf.write_data_to_file(p.jobs)
#endregion


