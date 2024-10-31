import os
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class VacancyParser:

    def __init__(self, site, wrong_words, companies, headless=True):
        self.town = os.getenv('TOWN')
        self.money = 80000
        print(f"Town: {self.town}")
        chrome_driver_path = os.getenv('CHROME_DRIVE_PATH')
        ser = Service(chrome_driver_path)
        op = webdriver.ChromeOptions()
        if headless:
            op.add_argument("--headless")
        op.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(service=ser, options=op)
        self.driver.get(site)
        self.wrong_words = wrong_words
        self.companies = companies

        self.times = ["годин", "години", "годину", "минут", "час", "No data", "дні", "днів", "день", "дня", "дней"]
        self.job_href = []
        self.jobs = []

    def filter(self):
        new_list = []
        for i in self.jobs:
            company = i['company'].lower().split(" ")
            title = i['job_title'].lower().split(" ")

            # period = i['period'].lower().split(" ")
            if not not set(company).isdisjoint(self.companies) \
                    and not not set(title).isdisjoint(self.wrong_words):
                new_list.append(i)

        self.jobs = new_list
        print(f"Filtered. Num: {len(self.jobs)}")

    def parser_robota_ua(self, hrefs):

        flag = True
        page = 1
        self.job_href += hrefs
        try:

            while flag:

                flag = False
                time.sleep(2)
                try:
                    for i in self.driver.find_elements(By.CSS_SELECTOR, "alliance-vacancy-card-desktop"):

                        if i and i.find_element(By.CSS_SELECTOR, "a").get_attribute("href") not in self.job_href:
                            title = i.find_element(By.CSS_SELECTOR, "a h2").text
                            company = i.find_element(By.CSS_SELECTOR, "span.santa-mr-20").text
                            href = i.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                            self.job_href.append(href)
                            # town = i.find_element(By.XPATH, "//span[2]").text
                            
                            remote = i.find_elements(By.CSS_SELECTOR,
                                                     "alliance-vac-list-status-label div.santa-bg-black-200")

                            remote_answer = False
                            if len(remote) > 0:
                                remote_answer = True

                            period_element = i.find_elements(By.CSS_SELECTOR,
                                                             "div.santa-justify-between div.santa-typo-secondary")

                            if len(period_element) > 0:
                                period_ = period_element[0].text
                                period = period_
                            else:
                                period_ = "No data"
                                period = period_
                            #     Remote jobs only
                            if remote_answer:
                                self.jobs.append(
                                    {"company": company, "job_title": title, "href": href, "period": period})
                            flag = True


                except Exception as ex:
                    flag = True
                    print("Middle try: ", ex)

                try:
                    time.sleep(2)
                    menu = self.driver.find_elements(By.CSS_SELECTOR, "alliance-vacancy-card-desktop a h2")

                    if (len(menu)) > 0:
                        ActionChains(self.driver).move_to_element(menu[-1]).scroll_by_amount(1, 1000).perform()
                    else:
                        time.sleep(2)
                        self.driver.execute_script("window.scrollBy(0, 100)")

                except Exception as ex:
                    print("Menu and Actionchains try: ", ex)

                if not flag:

                    time.sleep(2)
                    res = self.driver.find_elements(By.CSS_SELECTOR, "div.paginator div:not(.active)")
                    pages = [int(i.text) for i in res if i.text.isdigit()]
                   
                    if page + 1 in pages:
                        flag = True
                        element = [i for i in res if i.text == str(page + 1)][0]
                        self.driver.execute_script("window.scrollBy(0, -150)")
                        ActionChains(self.driver).move_to_element(element).click().perform()

                        print(f"Number on the {page} page: ", len(self.jobs))
                        page += 1



        except Exception as e:
            print("First try: ", e)

        finally:
            self.driver.quit()

        self.filter()

        return self.jobs

    def parser_work_ua(self, hrefs):

        flag = True
        page = 1
        self.job_href += hrefs
        try:
            while flag:

                time.sleep(2)
                flag = False
                for i in self.driver.find_elements(By.CSS_SELECTOR,
                                                   "div.card.card-hover.card-visited.job-link.wordwrap"):

                    title = i.find_element(By.CSS_SELECTOR, "h2 a").text
                    href = i.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
                    info = i.find_elements(By.CSS_SELECTOR, "div.add-top-xs span")
                    infos = [i.text for i in info if i.text != '']
                    vac = {"company": infos[0], "job_title": title, "href": href, "period": "", "town": infos[1]}

                    if (vac["town"] == "Дистанційно" or vac["town"] == self.town) and href not in self.job_href:
                        self.jobs.append(vac)
                        self.job_href.append(href)

                res = self.driver.find_elements(By.CSS_SELECTOR, "ul.pagination.hidden-xs a")
                pages = [int(i.text) for i in res if i.text.isdigit()]

                if page + 1 in pages:
                    flag = True
                    element = [i for i in res if i.text == str(page + 1)][0]
                    ActionChains(self.driver).move_to_element(element).click().perform()
                    print(f"Number on the {page} page: ", len(self.jobs))

                    page += 1

        except Exception as e:
            print("First try: ", e)

        finally:
            self.driver.quit()

        self.filter()
        return self.jobs

    def job_ua(self, hrefs):
        flag = True
        page = 1
        self.job_href += hrefs
        try:
            while flag:

                time.sleep(2)
                flag = False
                for i in self.driver.find_elements(By.CSS_SELECTOR,
                                                   "li.b-vacancy__item.js-item_list"):
                    if (len(i.find_elements(By.CSS_SELECTOR, "div.b-vacancy__top-inner h3"))) > 0:

                        # region Variables

                        money = i.find_elements(By.CSS_SELECTOR, "h3 span.b-vacancy__top__pay")
                        if len(money) > 0:
                            try:
                                money = int(money[0].text.replace(" ", "").split("грн")[0])
                            except Exception as e:
                                print("Money exception: ", e)
                        else:
                            money = 0

                        title = i.find_element(By.CSS_SELECTOR,
                                               "div.b-vacancy__top-inner h3 a.b-vacancy__top__title.js-item_title").text
                        href = i.find_element(By.CSS_SELECTOR, "a.b-vacancy__top__title.js-item_title").get_attribute(
                            "href")
                        company = i.find_element(By.CSS_SELECTOR, "span.link__hidden").text
                        town = i.find_element(By.CSS_SELECTOR, "span.b-vacancy__tech__item a.link__hidden").text

                        if (len(i.find_elements(By.CSS_SELECTOR, "span.b-vacancy__tech__item"))) > 4:
                            form = i.find_elements(By.CSS_SELECTOR, "span.b-vacancy__tech__item")[4].text

                        else:
                            form = "no data"
                        # endregion

                        vac = {"company": company, "job_title": title, "href": href, "period": "", "town": town,
                               "work_type": form}

                        if vac["town"] == self.town and href not in self.job_href and money < self.money:
                            self.jobs.append(vac)
                            self.job_href.append(href)
                            flag = True

                    self.driver.execute_script("window.scrollTo(0, 5300);")

                if not flag:
                    res = self.driver.find_elements(By.CSS_SELECTOR, "a.b-pager__link")
                    pages = [int(i.text) for i in res if i.text.isdigit()]

                    if page + 1 in pages:
                        flag = True
                        try:
                            element = [i for i in res if i.text == str(page + 1)][0]
                            ActionChains(self.driver).move_to_element(element).click().perform()
                        except Exception as e:
                            print("Getting in pages", e)
                        time.sleep(2)
                        print(f"Number on the {page} page: ", len(self.jobs))

                        page += 1

        except Exception as e:
            print("First try: ", e)

        finally:
            self.driver.quit()

        self.filter()
        return self.jobs
