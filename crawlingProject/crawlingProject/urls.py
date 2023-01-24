from django.contrib import admin
from django.urls import path
from articles import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('article/', views.article, name='article'),
    path('site-list/', views.getSiteList, name='siteList')
]
