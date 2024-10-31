from pprint import pprint
from time import sleep
import requests
from bs4 import BeautifulSoup


class VacancyPSoup:

    def __init__(self, link, wrong_words, companies, hrefs):
        self.wrong_words = wrong_words
        # self.link = link
        self.soup = self.get_soup(link=link)
        self.job_href = []
        self.job_href += hrefs
        self.jobs = []
        self.companies = companies

    def get_soup(self, link):
        response = requests.get(link)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def get_data_jooble(self):

        for i in self.soup.find_all("article"):
            try:
                a = i.find_next("a")

                title = a.getText("a")

                href = a.get('href')
                p = i.find_next("p", "Ya0gV9")

                if i.find("p"):
                    company = p.getText("p")

                if i.find("div", "caption e0VAhp"):

                    period = i.find_next(
                        "div", "caption e0VAhp").getText("div")

                if href not in self.job_href and self.filter(title=title, company=company):
                    vac = {"company": company, "job_title": title,
                           "href": href, "period": period, }
                    self.jobs.append(vac)
                    self.job_href.append(href)

            except Exception as e:
                print("get_data: ", e)

        print("Parsed and filtered jobs: ", len(self.jobs))

    def get_data_seek_au(self):
        url_prefix = "https://www.seek.com.au"
        flag = True
        page = 2

        while flag:
            flag = False

            for i in self.soup.find_all("article"):

                try:

                    a = i.find_next("a")
                    href = f"{url_prefix}{a.get('href')}"
                    title = i['aria-label']
                    company = i.find_next("a", "_842p0a0").getText("a")

                    if href not in self.job_href and self.filter(title=title, company=company):
                        vac = {"company": company, "job_title": title,
                               "href": href, "period": "", }
                        self.jobs.append(vac)
                        self.job_href.append(href)

                except Exception as e:
                    print("get_data_seek: ", e)
            print(f"Number on the {page-1} page: ", len(self.jobs))

            for i in self.soup.find_all("a", {"title": f"Go to page {page + 1}"}):
                next_page_link = f"{url_prefix}{i.get('href')}"
                self.soup = self.get_soup(next_page_link)
                flag = True
                page += 1
                break

        print("Filtered Seek.com.au jobs: ", len(self.jobs))

    def get_data_gumtree_au(self):
        url_prefix = "https://www.gumtree.com.au"

        anchors = self.soup.find_all("a", {"class": "user-ad-row-new-design"})

        for i in anchors:
            title = i.find(
                "span", {"class", "user-ad-row-new-design__title-span"}).getText()
            href = f"{url_prefix}{i.get('href')}"

            if href not in self.job_href and self.filter(title=title, company="No_company"):
                vac = {"company": "No_company", "job_title": title,
                       "href": href, "period": "", }
                self.jobs.append(vac)
                self.job_href.append(href)
                
        # not done functionality if number of page more then 24
        print("Parsed and filtered jobs: ", len(self.jobs))

    def get_data_olx_ua(self):
        url_prefix = "https://www.olx.ua"

        for i in self.soup.find_all("div",{"data-cy":"l-card"}):
            
            try:
                
                a = i.find_next("a")
                href = f"{url_prefix}{a.get('href')}"                
                title = i.h6.getText()
             

                if href not in self.job_href and self.filter(title=title, company=""):
                    vac = {"company": "", "job_title": title,
                           "href": href, "period": "", }
                    self.jobs.append(vac)
                    self.job_href.append(href)

            except Exception as e:
                print("get_data: ", e)

        print("Parsed and filtered jobs: ", len(self.jobs))
        



    def filter(self, title, company):

        arr_titles = title.lower().split(" ")
        arr_companies = company.lower().split(" ")
        if not not set(arr_companies).isdisjoint(self.companies) \
                and not not set(arr_titles).isdisjoint(self.wrong_words):
            return True
        return False
