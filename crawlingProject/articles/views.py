from django.shortcuts import render, redirect
from articles.models import Article
from .crawling import Crawling
def index(request):
    return render(request, 'index.html')
  
def create(request):
    crawling = Crawling()
    dataList = crawling.getMultiContents()
    for dataObject in dataList :        
        article = Article(title=dataObject["title"], published_datetime=dataObject["publishedDate"], body = dataObject["body"])
        article.save()
    return redirect('/')