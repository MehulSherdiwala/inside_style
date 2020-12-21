from django.urls import path

from . import views

urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.index, name="index"),
    path('registration/', views.registration, name="registration"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name="login"),
    path('ajax/load-cities', views.load_city, name="load_city"),
    path('ajax/load-state', views.load_state, name="load_state"),
]
