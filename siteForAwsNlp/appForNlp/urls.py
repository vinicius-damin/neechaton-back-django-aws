from django.urls import path
from . import views

app_name='appForNlp'

urlpatterns = [
    path('', views.index, name='index'),
    path('nlp_result', views.nlp_result, name='nlp_result')
]