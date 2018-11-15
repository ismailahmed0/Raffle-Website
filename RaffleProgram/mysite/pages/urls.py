from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('about/', views.about, name='about'),
    #path('contact/', views.contact, name='contact'),
    #path('testpage/', views.testpage, name='testpage'),
    path('purchase/', views.Purchase, name='purchase'),
    path('money/', views.Money, name='money'),

]
