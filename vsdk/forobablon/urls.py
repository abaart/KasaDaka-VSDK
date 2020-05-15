from django.conf.urls import url, include

from . import views

app_name= 'forobablon'
urlpatterns = [
    url(r'^results/$', views.resultsIndex, name='results'),
]