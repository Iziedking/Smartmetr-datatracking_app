from django.urls import path
from .import views

urlpatterns = [
     path('', views.getAbujaData, name='getAbujaData'),
 ]
