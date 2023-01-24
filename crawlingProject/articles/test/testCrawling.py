from django.test import TestCase
from articles.crawling import Crawling
import unittest
import dateparser
class Selenium(TestCase) :
    # 크롤링 된 데이터 중 null 값으로 넘어온 카운트 반환
    def getNullValueCount(self, objectList, key):
        nullValueCount = 0
        for object in objectList :
            if object[key] == '':
                nullValueCount += 1
        return nullValueCount
    @unittest.skip
    def testSchoolNoticeCrawling(self) :
        crawlingTest = Crawling(
            siteUrl="https://school.iamservice.net/organization/1674/group/2001892",
            linkList='/html/body/div[1]/div[2]/div/section/div[*]/div[1]/a',
            title='/html/body/section/section/section/div[2]/div[1]',
            publishedDate='/html/body/section/section/section/div[1]/div[3]/div[2]/div',
            body='//*[@id="articleBody"]',
            attachmentList='/html/body/section/section/section/div[2]/div[2]/div[2]',
            excludePathList=''
        )
        self.assertEqual( self.getNullValueCount(crawlingTest.getMultiContents([''] , 5 ), 'title') , 0 )
    
    @unittest.skip
    def testNaverBlogCrawling(self) :
        crawlingTest = Crawling(
            siteUrl="https://blog.naver.com/PostList.naver?from=postList&blogId=sntjdska123&categoryNo=51",
            linkList='//*[@id="PostThumbnailAlbumViewArea"]/ul/li[*]/a',
            title='/html/body/div[8]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[8]/div[1]/div/table[2]/tbody/tr/td[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/p/span',
            publishedDate='/html/body/div[8]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[8]/div[1]/div/table[2]/tbody/tr/td[2]/div[1]/div/div[1]/div[2]/div/div[3]/span[2]',
            body='/html/body/div[8]/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[8]/div[1]/div/table[2]/tbody/tr/td[2]/div[1]/div/div[2]',
            attachmentList='',
            excludePathList=''
        )
        self.assertEqual( self.getNullValueCount(crawlingTest.getMultiContents([''], 5), 'title') , 0 )
    @unittest.skip
    def testBBCNewsCrawling(self) :
        crawlingTest = Crawling(
            siteUrl="http://feeds.bbci.co.uk/news/rss.xml",
            linkList='/html/body/div[3]/div[1]/div/div[*]/ul/li/a',
            title='/html/body/div[2]/div/main/div[5]/div/div[1]/article/header/h1',
            publishedDate='/html/body/div[2]/div/main/div[5]/div/div[1]/article/header/div[1]/ul/div/li/div[2]/span/span/time',
            body='/html/body/div[2]/div/main/div[5]/div/div[1]',
            attachmentList='',
            excludePathList='/html/body/div[2]/div/main/div[5]/div/div[1]/article/header'
        )
        self.assertEqual( self.getNullValueCount(crawlingTest.getMultiContents([''], 5), 'title') , 0 )
    @unittest.skip
    def testTimeZone(self):     
        print(dateparser.parse('01-13', settings={'TIMEZONE': '+0900'}))
        print(dateparser.parse('Just now'))
        

        
        
