from django.conf.urls import url, include

from . import views

app_name= 'forobablon'
urlpatterns = [
    url(r'^results/$', views.resultsIndex, name='results-index'),
    url(r'^results/(?P<date>\d{4}-\d{2}-\d{2})$', views.results, name='results'),
]

