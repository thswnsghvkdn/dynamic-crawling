from django.shortcuts import render, redirect
from articles.models import Article
from articles.models import FailureLink
from articles.models import Xpath
from articles.models import excludeXpath
from .crawling import Crawling
from django.http import HttpResponse
from django.core import serializers
import dateparser
import json
# 처음 화면 렌더링
def index(request):
    # 이미 저장 되어 있는 테스트 케이스 
    siteList = Xpath.objects.all()
    context = {
        'siteList': siteList
    }
    return render(request, 'index.html', context)
# 크롤링 작업
def create(request):    
    # 크롤링 작업에 필요한 xpath를 인자로 넘긴다.
    crawling = Crawling(
            siteUrl=request.POST['siteUrl'],
            linkList=request.POST['linkList'],
            title=request.POST['title'],
            publishedDate=request.POST['publishedDate'],
            body=request.POST['body'],
            attachmentList=request.POST['attachmentList'],
            excludePathList=json.loads(request.POST['excludePathList']) ,
        )
    existsLinks = getExistsLinkList(request.POST['siteName']) # 제외시킬 이미 존재 하는 url
    dataList = crawling.getMultiContents(existsLinks, int(request.POST['crawlingCount'])) # 크롤링 작업 결과 객체 list
    for dataObject in dataList : 
        # 필수 값이 없을 경우 실패 테이블에 저장
        if checkResultHasNull(dataObject) :       
            fail = FailureLink(
            url = dataObject["url"],
            site_name = request.POST['siteName']
            )
            fail.save()
        else : 
            # 성공시에 article 테이블에 데이터들을 저장한다.
            article = Article(
            url = dataObject["url"],
            title=dataObject["title"], 
            published_datetime=dateparser.parse(dataObject["publishedDate"], settings={'TIMEZONE': request.POST['timezone']}), 
            body = dataObject["body"],
            attachment_list = dataObject["attachmentList"],
            site_name = request.POST['siteName']
            )
            try : 
                article.save()
            except :
                # 저장시 문제가 발생할 경우 실패 테이블에 저장
                fail = FailureLink(
                url = dataObject["url"],
                site_name = request.POST['siteName']
                )
                fail.save()
    return redirect('/')

# db 에 저장된 값을 가져온다.
def read(request):
    # 호면에서 넘긴 site 이름의 데이터들만 가져온다.
    articles = Article.objects.filter(site_name = request.GET['siteName'] )
    jsonPost = serializers.serialize('json', articles)
    return HttpResponse(jsonPost, content_type="text/json-comment-filtered")

# 옵션에서 테스트 케이스를 선택할 경우 해당 xpath 들을 db에서 가져온다.  
def getSiteList(request):
    # 크롤링할 xpath
    siteXpath = list(Xpath.objects.filter(site_name = request.GET['siteName']).values())
    # 제외될 원소 리스트
    excludeList = list(excludeXpath.objects.filter(site_name = request.GET['siteName']).values())
    context = {
        'siteXpath' : siteXpath,
        'excludeList' : excludeList
    }
    data = json.dumps(context)
    return HttpResponse(data, content_type="text/json-comment-filtered")

# 사이트 이름을 기준으로 이미 진행했던 link list 반환
def getExistsLinkList(siteName) :
    existLinkList = []
    resultObjectList = list(Article.objects.filter(site_name = siteName ).only("url").values())
    for object in resultObjectList :
        existLinkList.append(object['url'])
    return existLinkList
# 객체 필수값에 값이 있는지 여부 검사
def checkResultHasNull(dataObject) :
    importantKeys = ['title', 'body']
    for key in importantKeys :
        try :
            valueLength = len(dataObject[key])
            if valueLength < 1 :
                return True
        except :
            return True
    return False
