from django.contrib import admin
from django.urls import path, re_path, include
from apps.epidemic_map import views

app_name = 'epidemic'
urlpatterns = [
    path('epidemic/', views.epidemic, name='epidemic'),
    path('get_map_data/', views.get_map_data, name='get_map_data'),
    path('get_ncov_totalcount/', views.get_ncov_totalcount, name='get_ncov_totalcount'),
    path('get_everyday_data/', views.get_everyday_data, name='get_everyday_data'),
    path('DA_epidemic/', views.epidemic_DA_index, name='DA_epidemic'),
]
