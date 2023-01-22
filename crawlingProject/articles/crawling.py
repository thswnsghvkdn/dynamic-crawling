from selenium import webdriver
from selenium.webdriver.common.by import By
from multiprocessing import Pool
from selenium.webdriver.chrome.options import Options

# 직렬화가 되지 않아 임시적으로 전역으로 선언하여 처리
op = Options()
op.headless = True
chrome = webdriver.Chrome(options=op)
def getElementTextByXpathOrNull(driver , xPath) :
    innerTextData = ""
    try:
        innerTextData = driver.find_element(By.XPATH, xPath).get_attribute('innerText')
    except:
        return ""
    return innerTextData

class Crawling:
    def __init__(self, siteUrl, linkList, title, publishDate, body, attachmentList) :
        self.siteUrl = siteUrl
        self.linkList = linkList
        self.title = title
        self.publishDate = publishDate
        self.body = body
        self.attachmentList = attachmentList

    def getSinglecontent(self, link):
        chrome.get(link)
        title = getElementTextByXpathOrNull(chrome, self.title)
        publishedDate = getElementTextByXpathOrNull(chrome, self.publishDate)
        body = getElementTextByXpathOrNull(chrome, self.body)
        attachmentList = getElementTextByXpathOrNull(chrome, self.attachmentList)
        contentObject = {"title": "", "publishedDate": "", "body": "", "attachmentList": ""}
        contentObject["title"] = title
        contentObject["publishedDate"] = publishedDate
        contentObject["body"] = body
        contentObject["attachmentList"] = attachmentList
        return contentObject
    
    def getMultiContents(self):
        chrome = webdriver.Chrome(options=op)
        chrome.get(self.siteUrl)
        linkObjects = chrome.find_elements(By.XPATH, self.linkList)
        linkList = []
        for linkObject in linkObjects :
            linkList.append(linkObject.get_attribute('href'))
        with Pool(processes=4) as pool:
            contentList = pool.map(self.getSinglecontent, linkList)
            return contentList

        
