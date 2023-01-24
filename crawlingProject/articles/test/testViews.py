from django.test import TestCase
from django.test import Client
import dateparser
import unittest
class Ajax(TestCase) :
    @unittest.skip
    def testBasicInput(self) :
        client = Client()
        response = client.post('/create/', {
            'siteName' : '수내초등학교',
            'siteUrl' : "https://school.iamservice.net/organization/1674/group/2001892",
            'linkList' :'/html/body/div[1]/div[2]/div/section/div[1]/div[1]/a',
            'title' : '/html/body/section/section/section/div[2]/div[1]',
            'publishDate': '/html/body/section/section/section/div[1]/div[3]/div[2]/div',
            'body' : '//*[@id="articleBody"]',
            'attachmentList' : '/html/body/section/section/section/div[2]/div[2]/div[2]',
            'excludePathList' : '',
        })
        print(response)
