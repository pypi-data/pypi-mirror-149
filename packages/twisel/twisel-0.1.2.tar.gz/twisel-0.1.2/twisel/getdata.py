from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import warnings
warnings.filterwarnings("ignore")
import time

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

    def setKeyword(self):
        spliting = self.keyword.split()
        joining = '%20'.join(spliting)
        searching = f'%22{joining}%22'

        return searching

    def setPopuler(self):
        if self.populer == False:
            populer = '&f=live'
        else:
            populer = ''

        return populer

    def setUntil(self):
        if self.until != '':
            until = f'%20until%3A{self.until}'
        else:
            until = ''

        return until

    def setSince(self):
        if self.since != '':
            since = f'%20since%3A{self.since}'
        else:
            since = ''

        return since

    def setSrc(self):
        if self.until != '' or self.since != '':
            src = 'typed_query'
        else:
            src = 'recent_search_click'

        return src


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
        if self.keyword == '':
            raise CustomError('Keyword not Valid!')
        else:
            driver = self.getDriver()
            driver.get(f'https://twitter.com/search?q={self.setKeyword()}{self.setUntil()}{self.setSince()}&src={self.setSrc()}{self.setPopuler()}')
            kata = []
            layar = 0


            while True:
                huruf = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.css-1dbjc4n article')))
                temukan = driver.find_elements(By.CSS_SELECTOR,'.css-1dbjc4n .css-901oao.r-18jsvk2.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0')
                nama = driver.find_elements(By.CSS_SELECTOR,'.css-901oao.r-1awozwy.r-18jsvk2.r-6koalj.r-37j5jr.r-a023e6.r-b88u0q.r-rjixqe.r-bcqeeo.r-1udh08x.r-3s2u2q.r-qvutc0')
                username = driver.find_elements(By.CSS_SELECTOR,'.css-901oao.css-bfa6kz.r-14j79pv.r-18u37iz.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0 .css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0')
                times = driver.find_elements(By.TAG_NAME, 'time')

                if len(kata) > self.tweets:
                    break

                for i, j, l, c  in zip(nama, temukan, username, times):
                    jr = j.text.replace('\n', ' ')
                    kata.append({'name': i.text,'username':l.text, 'tweet': jr,'time':c})


                last_height = driver.execute_script("return document.body.scrollHeight")
                if int(layar) - 720  == int(last_height) :
                    driver.close()
                    break


                layar = int(last_height) + 720
                driver.execute_script(f"window.scrollTo(0, {layar});")
                time.sleep(0.5)

            val = []
            for i in kata:
                if i['tweet'] in val:
                    kata.remove(i)
                else:
                    val.append(i['tweet'])


            return kata[:self.tweets]


