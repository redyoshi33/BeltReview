from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.regis),
    url(r'^login$', views.login),
    url(r'^books$', views.bookhome),
    url(r'^books/add$', views.addbook),
    url(r'^books/submit$', views.submit),
    url(r'^books/reviews/(?P<id>\d+)$', views.reviews),
    url(r'^books/reviews/delete/(?P<id>\d+)$', views.delete),
    url(r'^logout', views.logout),
    url(r'^books/(?P<id>\d+)$', views.showbook),
    url(r'^users/(?P<id>\d+)$', views.users),
]