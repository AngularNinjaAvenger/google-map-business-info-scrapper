from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re,math,bs4,requests,validators

print("starting......")


class Get:
    def __init__(self):
        self.names = []
        self.laststopped = 0
        self.loaded = False
        self.email = self.get_email()
        self.facebook = self.get_facebook()
        self.twitter = self.get_twitter()
        self.linkedin = self.get_linkedin()
        self.email_result = []
        self.facebook_result = []
        self.twitter_result = []
        self.linkedin_result = []
    def main(self,files,info):
        self.nitch = info["nitch"]
        self.location = info["location"]
        print("running main..........")
        chromedriver = 'C:/users/angular_nija_avenger/downloads/chromedriver'
        try:
            driver = webdriver.Chrome(chromedriver)
            self.browser = driver
        except:
            print("something went wrong running the browser")
        # lst_stp = input("enter Last stopped:  ")
        # try:
        #     self.laststopped = int(lst_stp)
        # except:
        #     self.laststopped = 0
        self.laststopped = 0
        self.load_names(files,self.validate())
        self.fill_sheet()
    def load_names(self,files,regex):
        x = pd.read_csv(files)
        size = int(f"{x.size}")
        for i in range(math.floor(size/2)):
            if self.laststopped >= i:
                if not self.loaded:
                    self.loaded = True
                    # CALL LOAD METHOD HERE
                continue
                        
            br = self.browser
            index = "0"
            br.get(f"https://www.google.com/maps/search/{x.loc[i][index]}")
            sleep(20)
            self.checkList(br)
            self.get_info(br.page_source,regex,i)
    def validate(self):
        return re.compile(r'\s*([^:\/\n]+\.com)\s*')
         
    def get_info(self,page_source,regex,c_index):
        x = validators
        general = self.get_general(page_source)
        url = None
        for i in general:
            for item in i:
                temp = f"http://{item}"
                if x.url(temp) == True:
                    url = item
        name = self.get_name(page_source)
        images = self.get_images(page_source)
        rating = self.get_rating(page_source)            
        business = {
                "name":self.get_name(page_source)[0],
                "images":self.get_images(page_source)[0],
                "rating":self.get_rating(page_source)[0],
                "website":url,
        }
        # del business["images"]
        # print(business)
        if url:
            website_code = str(self.get_site_code_bs4(business["website"]))
            f_s = self.facebook.search(website_code)
            t_s  = self.twitter.search(website_code)
            e_s = self.email.search(website_code)
            l_s = self.linkedin.search(website_code)
            if f_s and f_s.group(0):
                business["contact_mf"] = "FACEBOOK"
                business["contact_df"] = f_s.group(0)
                self.facebook_result.append(business)
            if t_s and t_s.group(0):
                business["contact_mt"] = "TWITTER"
                business["contact_dt"] = t_s.group(0)
                self.twitter_result.append(business)
            if e_s and e_s.group(0):
                business["contact_me"] = "EMAIL"
                business["contact_de"] = e_s.group(0)
                self.email_result.append(business)
            if l_s and l_s.group(0):
                business["contact_ml"] = "LINKEDIN"
                business["contact_dl"] = l_s.group(0)
                self.linkedin_result.append(business)
            if c_index % 20:
                self.fill_sheet()
        else:
            return 
    def fill_sheet(self):
        print("filling sheet ..............................")
        if self.facebook_result:
            f = pd.DataFrame(self.facebook_result)
            f_r = f[["name","website","rating","images","contact_mf","contact_df"]]
            f_r.to_csv(f"fb_{self.nitch}_{self.location}_leads.csv")
        if self.twitter_result:
            t = pd.DataFrame(self.twitter_result)
            t_r = t[["name","website","rating","images","contact_mt","contact_dt"]]
            t_r.to_csv(f"tw_{self.nitch}_{self.location}_leads.csv")
        if self.linkedin_result:
            l = pd.DataFrame(self.linkedin_result)
            l_r = l[["name","website","rating","images","contact_me","contact_de"]]
            l_r.to_csv(f"ln_{self.nitch}_{self.location}_leads.csv")
        if self.email_result:
            e = pd.DataFrame(self.email_result)        
            e_r = e[["name","website","rating","images","contact_me","contact_de"]]
            e_r.to_csv(f"em_{self.nitch}_{self.location}_leads.csv")
        print("filled sheet ..............................")
    def get_site_code_bs4(self,site):
        print("trying to get thier website code")
        print(site,"<--this is thier website")
        url= 'https://' + site
        try:
            res = requests.get(url,{"accepts":"text/html"})
            soup = bs4.BeautifulSoup(res.text,'html.parser')
            store = soup.select("html")
            if store:
                print("gotten with bs4")
                return store[0]
            else:
                return False
        except:
            print("couldnotfind with bs4 want tot try selenium")
            return self.get_site_code_sel(site)
    def validate_website(self,website):
        pass
    def get_site_code_sel(self,site):
        x = self.browser.get('https://' + site)
        delay = 5 # seconds
        try:
            myElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#section-title > div > h1')))
            return self.browser.page_source
        except TimeoutException:
            if self.browser.page_source:
                return self.browser.page_source
            return "no code found"

    def get_name(self,page_source):
        x = re.compile(r'<h1 jstcache=\"\d*\" class="GLOBAL__gm2-headline-5 section-hero-header-title-title" jsan="7.GLOBAL__gm2-headline-5,7.section-hero-header-title-title">(.*?)</h1>')
        if x.findall(page_source):
            return x.findall(page_source)
        else:
            return ["NO NAME FOUND"]
    def get_general(self,page_source):
        x = re.compile(r'<span jstcache=\"\d*\" class="widget-pane-link" jsan="7.widget-pane-link">((.*?))</span>')
        if x.findall(page_source):
            print(x.findall(page_source),"<=====PAGE SOURCE")
            return x.findall(page_source)
        else:
            return [
            ["NO ADDRESS FOUND"],
            ["NO LOCATION FOUND"],
            ["NO WEBSITE FOUND"],
            ["NO NUMBER FOUND"]
            ]
    def get_images(self,page_source):
        x = re.compile(r'<div jstcache=\"\d*\" class="section-hero-header-image">((.*?))</div>')
        if x.findall(page_source):
            return x.findall(page_source)
        else:
            return [
            "NO IMAGE COULD BE FOUND"
            ]
    def get_rating(self,page_source):
        x = re.compile(r'<div jstcache=\"\d*\" class="gm2-display-2" jsan="7.gm2-display-2">(.*?)</div>')
        if x.findall(page_source):
            return x.findall(page_source)
        else:
            return ["0.0 NO RATING FOUND"]
    def checkList(self,br):
        g = self.checkListReg().findall(br.page_source)
        if g:
            print("yes the website has a list of links")
            try:
                x = br.find_element_by_css_selector("#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div.section-layout.section-scrollbox.scrollable-y.scrollable-show.section-layout-flex-vertical > div:nth-child(1)")
                x.click()
                print("clicked it")
                sleep(20)
            except:
                return

    def checkListReg(self):
        x = re.compile(r"<span jstcache=\"\d*\">(\w.*?)</span>")
        return x
    def checkForSuggestions(self,br):
        try:
            x = br.find_by_css_selector('#omnibox-singlebox > div.gstl_50.sbdd_a > div:nth-child(2) > div.sbdd_b > div > ul > li:nth-child(1)').click()
            sleep(10)
            return True
        except:
            return False
            pass
    def get_email(self):
        client_email = re.compile(u"([a-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)", re.IGNORECASE)
        return client_email
    def get_twitter(self):
        twitter_search = re.compile(r"twitter.com/\w+", re.IGNORECASE)
        return twitter_search
    def get_facebook(self):
        facebook_search = re.compile(r"facebook.com/\w+", re.IGNORECASE)
        return facebook_search
    def get_linkedin(self):
        linkedin_search = re.compile(r"linkedin.com/company/\w+", re.IGNORECASE)
        return linkedin_search


load = Get()
# load = Get().main("",{
#     "nitch":"doctors",
#     "location":"new york"
# })






    




