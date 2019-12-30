from selenium import webdriver
from time import sleep
import pandas as pd
from Get_info import load
import re

class Gmap:
    def __init__(self):
        self.browser = None
        self.names = []
        self.nitch = None
        self.location = None
        self.there_is_a_next_button = True
        self.fixedLastStop = False
        pass
    def main(self,nitch,location):
        self.nitch = nitch
        self.location = location
        self.last_stopped = input("Last stop if None Enter (0): ")
        try:
            self.last_stopped = int(last_stopped)
        except:
            self.last_stopped = 0
        print(type(self.last_stopped))
        if self.last_stopped > 0:
            self.load()
        self.initBrowser()
        self.lunch_site_search(nitch,location)
        sleep(20)
        while self.there_is_a_next_button:
            self.get_names(self.gps())
            self.click_next_button()
            print(self.names,len(self.names))
        return True
        # load(f'maps_{self.nitch}_{self.location}_data.csv')
    def gps(self):
        return self.browser.page_source
    def click_next_button(self):
        try:
            next_button = self.x.find_element_by_css_selector("#n7lv7yjyC35__section-pagination-button-next > span")
            if  not next_button:
                self.there_is_a_next_button = False
                return
            next_button.click()
        except:
            self.there_is_a_next_button = False
        sleep(20)
    def load(self):
        print("load method called")
        try:
            x = pd.read_csv(f'maps_{self.nitch}_{self.location}_data.csv')
            for i in x["0"]:
                self.names.append(i)
        except:
            return
        print("load method called successfully")
        print(self.names)
    def lunch_site_search(self,nitch,location):
        x = self.browser
        brow = x.get("https://www.google.com/maps")
        sleep(20)

        while not len(x.page_source) > 1000:
            brow = x.get("https://www.google.com/maps")
        inputField = x.find_element_by_css_selector('#searchboxinput')
        inputField.click()
        sleep(5)
        inputField.send_keys(f"{nitch} in {location}")
        sleep(3)
        x.find_element_by_css_selector('#searchbox-searchbutton').click()
        sleep(20)
        self.x = x
    def initBrowser(self):
        chromedriver = 'C:/users/angular_nija_avenger/downloads/chromedriver'
        driver = webdriver.Chrome(chromedriver)
        self.browser = driver
    def get_names(self,pg_source):
        if not self.fixedLastStop:
            self.fixedLastStop = True
            for i in range(self.last_stopped):
                self.click_next_button()
        m = re.compile(r"<span jstcache=\"\d*\">(\w.*?)</span>")
        result = m.findall(pg_source)
        if not len(result) > 5:
            return
        result.pop()
        result.pop()
        del result[0]
        for i in result:
            self.names.append(i)
        m_names = pd.DataFrame(pd.Series(self.names))
        m_names.to_csv(f'maps_{self.nitch}_{self.location}_data.csv')
# Gmap().main("doctors","new york the bronx")

getNames = Gmap

# f'maps_{self.nitch}_{self.location}_data.csv'







# prev = []





