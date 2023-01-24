from django.contrib import admin
from django.urls import path
from articles import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('create/', views.create, name='create'),
    path('read/', views.read, name='read'),
    path('site-list/', views.getSiteList, name='siteList')
]
