from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_redirect, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/places/', views.get_places, name='get_places'),
    path('api/data/', views.get_place_data, name='get_place_data'),
    path('rainwater-harvesting/', views.rainwater_harvesting, name='rainwater_harvesting'),
    path('save-user-place/', views.save_user_place, name='save_user_place'),
]
