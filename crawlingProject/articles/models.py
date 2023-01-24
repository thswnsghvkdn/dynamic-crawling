from django.db import models
# 크롤링 후 결과 값 
class Article(models.Model):
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    body = models.TextField()
    attachment_list = models.TextField()
    published_datetime = models.DateTimeField()
    updated_datetime = models.DateTimeField(auto_now = True)
    site_name = models.CharField(max_length=100)
    class Meta:  
        db_table = "article_tbl"
# 크롤링 할 XPATH
class Xpath(models.Model):
    site_name = models.CharField(max_length=20, default='')
    url = models.CharField(max_length=200, default='')
    link_list = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200, default='')
    body = models.CharField(max_length=200, default='')
    attachment_list = models.CharField(max_length=200, default='')
    published_date = models.CharField(max_length=200, default='')
    time_zone = models.CharField(max_length=10, default='')
    class Meta:  
        db_table = "xpath_tbl"
# BODY HTML 에서 제외시킬 ELEMENT
class excludeXpath(models.Model):
    site_name = models.CharField(max_length=20, default='')
    exclude_element_xpath = models.CharField(max_length=200, default='')
    class Meta:  
        db_table = "exclude_element_tbl"
# 데이터 크롤링을 제대로 해오지 못한 url 
class FailureLink(models.Model):
    site_name = models.CharField(max_length=20, default='')
    url = models.CharField(max_length=200)
    class Meta:  
        db_table = "failure_link_tbl"
        