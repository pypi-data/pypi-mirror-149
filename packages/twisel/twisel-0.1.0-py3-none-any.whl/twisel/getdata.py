from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

class CustomError(Exception):
    pass

class SearchTwitter:
    def __init__(self):
        self.PATH = r'c:'
        self.browser = 'chrome'
        self.keyword = ''
        self.until = ''
        self.since = ''
        self.populer = True
        self.tweets = 100

    def getDriver(self):

        if self.browser == 'chrome':
            return webdriver.Chrome(executable_path=self.PATH)
        elif self.browser == 'edge':
            return webdriver.Edge(executable_path= self.PATH)
        elif self.browser == 'firefox':
            return webdriver.Firefox(executable_path=self.PATH)
        elif self.browser == 'IE':
            return webdriver.Ie(executable_path=self.PATH)
        elif self.browser == 'safari':
            return webdriver.Safari(executable_path=self.PATH)

    def search(self):
        spliting = self.keyword.split()
        joining = '%20'.join(spliting)
        searching = f'%22{joining}%22'

        if self.until != '' or self.since != '':
            src = 'typed_query'
        else:
            src = 'recent_search_click'


        if self.populer == False:
            populer = '&f=live'
        else:
            populer = ''



        if self.until != '':
            until = f'%20until%3A{self.until}'
        else:
            until = ''


        if self.since != '':
            since = f'%20since%3A{self.since}'
        else:
            since = ''


        if self.keyword == '':
            raise CustomError('Keyword not Valid!')
        else:
            driver = self.getDriver()
            driver.get(f'https://twitter.com/search?q={searching}{until}{since}&src={src}{populer}')
            kata = []
            k = 0
            while True:
                huruf = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.css-1dbjc4n article')))
                temukan = driver.find_elements(By.CSS_SELECTOR,'.css-1dbjc4n .css-901oao.r-18jsvk2.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0')
                nama = driver.find_elements(By.CSS_SELECTOR,'.css-901oao.r-1awozwy.r-18jsvk2.r-6koalj.r-37j5jr.r-a023e6.r-b88u0q.r-rjixqe.r-bcqeeo.r-1udh08x.r-3s2u2q.r-qvutc0')

                if len(kata) > self.tweets:
                    break

                if len(kata) != 0 and len(temukan) != 0:
                    if kata[-1]['tweet'] == temukan[-1].text:
                        break

                for i, j in zip(nama, temukan):
                    jr = j.text.replace('\n', ' ')
                    kata.append({'nama': i.text, 'tweet': jr})


                # last_height = driver.execute_script("return document.body.scrollHeight")
                k += 720
                driver.execute_script(f"window.scrollTo(0, {k});")
                time.sleep(0.5)

            val = []
            for i in kata:
                if i['tweet'] in val:
                    kata.remove(i)
                else:
                    val.append(i['tweet'])

            driver.close()
            return kata[:self.tweets]

