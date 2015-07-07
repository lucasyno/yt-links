"""yt_links URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from links.views import StartPageView, YTLinksListAndCreateView, EditUserView, YTLinksDeleteView 


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', StartPageView.as_view(), name="start"),
    url(r'^your-links/(?P<gen_hash>\w+)/$', YTLinksListAndCreateView.as_view(), name='list'),
    url(r'^your-links/(?P<gen_hash>\w+)/edit_user/$', EditUserView.as_view(), name='edit_user'),
    url(r'^your-links/(?P<gen_hash>\w+)/(?P<video_id>[\w\+%-_& ]+)/delete/$', YTLinksDeleteView.as_view(), name='delete'),
]
