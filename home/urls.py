from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^contact$', views.contact, name='contact'),
    url(r'^about$',views.about,name='about'),
    url(r'^blog$',views.blog,name='blog'),
    url(r'^departments$',views.departments,name='departments')
]