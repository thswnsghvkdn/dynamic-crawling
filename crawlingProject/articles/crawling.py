from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
from time import time, sleep
from multiprocessing import Pool
from selenium.webdriver.chrome.options import Options

op = Options()
op.headless = True
chrome = webdriver.Chrome(options=op)
class Crawling:
    def __init__(self) :
        pass
    def getSinglecontent(self, link):
        chrome.get(link)   
        title = chrome.find_element(By.XPATH, '/html/body/section/section/section/div[2]/div[1]').get_attribute('innerText')
        publishedDate = chrome.find_element(By.XPATH, '/html/body/section/section/section/div[1]/div[3]/div[2]/div').get_attribute('innerText')
        body = chrome.find_element(By.XPATH, '//*[@id="articleBody"]').get_attribute('innerText')
    #   atachmentList = chrome.find_element(By.XPATH, '//*[@id="__content"]/div[2]/div[1]').get_attribute('innerText')
        contentObject = {"title": "", "publishedDate": "", "body": "", "atachmentList": ""}
        contentObject["title"] = title
        contentObject["publishedDate"] = publishedDate
        contentObject["body"] = body
        return contentObject
    
    def getMultiContents(self):
        chrome.get('https://school.iamservice.net/organization/1674/group/2001892')
        linkObjects = chrome.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/section/div[1]/div[1]/a')
        linkList = []
        for linkObject in linkObjects :
            linkList.append(linkObject.get_attribute('href'))
        with Pool(processes=4) as pool:
            # 여러 링크를 한번에 처리 하도록 링크 리스트와 처리함수를 pool 로 mapping 시킨다 
            contentList = pool.map(self.getSinglecontent, linkList)
            return contentList
