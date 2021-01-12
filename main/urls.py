from django.urls import path

from . import views

urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),
    path('registration/', views.registration, name="registration"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('ajax/load-cities', views.load_city, name="load_city"),
    path('ajax/load-state', views.load_state, name="load_state"),
    path('ajax/fetch_pdt', views.fetch_pdt, name="fetch_pdt"),
    path('ajax/load-creator/<ins_by>', views.load_creator, name="load_creator"),
    path('contact/', views.contact, name="contact"),
    path('designs/', views.designs, name="designs"),
    path('user_dashboard/', views.user_dashboard, name="user_dashboard"),
    path('product_list/', views.product_list, name="product_list"),
    path('product/<pdt_id>', views.product, name="product"),
    path('cart/', views.cart, name="cart"),
    path('ajax/addtocart', views.addtocart, name="addtocart"),
    path('ajax/addtocart/update', views.update_addtocart, name="update_addtocart"),
    path('product_list/', views.product_list, name="product_list"),

    path('admin/design_element/', views.design_element, name="design_element"),
]
