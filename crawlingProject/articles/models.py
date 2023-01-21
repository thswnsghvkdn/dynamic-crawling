from django.db import models

class Article(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    body = models.TextField()
    attachment_list = models.CharField(max_length=70)
    published_datetime = models.DateTimeField(auto_now_add = True)
    updated_datetime = models.DateTimeField(auto_now = True)
    site_name = models.CharField(max_length=20)
    class Meta:  
        db_table = "article_tbl"