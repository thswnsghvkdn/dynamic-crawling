from selenium import webdriver
from selenium.webdriver.common.by import By
from multiprocessing import Pool
from selenium.webdriver.chrome.options import Options

# 직렬화가 되지 않아 임시적으로 전역으로 선언하여 처리
op = Options()
op.headless = True
op.add_argument('user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
chrome = webdriver.Chrome(options=op)
# 제외시킬 원소 script 를 이용하여 제거
def deleteElementByXpath(driver, xPathList):
    script = ''
    for xPath in xPathList :
        try :
            script = "document.evaluate('" + xPath + "', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.remove();"
            driver.execute_script(script)
        except :
            pass

def getBodyHTMLByXpathOrNull(driver , xPath, excludePathList) :
    # 제외 시킬 element를 제거 한 이후에 body HTML 을 크롤링한다.
    deleteElementByXpath(driver, excludePathList)
    innerTextData = ""
    try:
        innerTextData = driver.find_element(By.XPATH, xPath).get_attribute('outerHTML')
    except:
        return ""
    return innerTextData

def getTextByXpathOrNull(driver , xPath) :
    innerTextData = ""
    try:
        innerTextData = driver.find_element(By.XPATH, xPath).get_attribute('innerText')
    except:
        return ""
    return innerTextData

class Crawling:
    def __init__(self, siteUrl, linkList, title, publishedDate, body, attachmentList = '', excludePathList = '' ) :
        self.siteUrl = siteUrl
        self.linkList = linkList
        self.title = title
        self.publishedDate = publishedDate
        self.body = body
        self.attachmentList = attachmentList
        self.excludePathList = excludePathList


    def getSinglecontent(self, link):
        chrome.get(link)
        title = getTextByXpathOrNull(chrome, self.title)
        publishedDate = getTextByXpathOrNull(chrome, self.publishedDate)
        attachmentList = getTextByXpathOrNull(chrome, self.attachmentList)
        body = getBodyHTMLByXpathOrNull(chrome, self.body , self.excludePathList)

        contentObject = {"url" : "", "title": "", "publishedDate": "", "body": "", "attachmentList": ""}
        contentObject["url"] = link
        contentObject["title"] = title
        contentObject["publishedDate"] = publishedDate
        contentObject["body"] = body
        contentObject["attachmentList"] = attachmentList
        return contentObject
    
   # 이미 진행했던 링크 리스트와 진행할 크롤링 횟수를 인자로 받는다.
    def getMultiContents(self, alreadyExistsLinks, crawlingCount):
        chrome = webdriver.Chrome(options=op)
        chrome.get(self.siteUrl)
        linkObjects = chrome.find_elements(By.XPATH, self.linkList)
        linkList = []
        for linkObject in linkObjects :
            link = linkObject.get_attribute('href')
            # 이미 진행되었던 LIST 안에 존재 하지 않을 경우만 LIST에 추가
            if link not in alreadyExistsLinks :
                linkList.append(link)
            # 한번에 진행할 크롤링 횟수만큼 LIST를 추가한다.
            if len(linkList) >= crawlingCount :
                break 
        # 링크리스트의 각 링크들을 개별 쓰레드가 접근하여 크롤링을 진행한다.
        with Pool(processes=4) as pool:
            # 첫번째로 받은 함수의 return 값들이 list로 묶여 반환된다. 
            contentList = pool.map(self.getSinglecontent, linkList)
            return contentList

        
