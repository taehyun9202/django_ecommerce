from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("base",views.base),
    path("search", views.search),
    path("search/<searchtext>", views.searchedItem),
    path("category/<bycategory>", views.byCategory),
    path("signup", views.signup),
    path("register", views.register),
    path("signin", views.signin),
    path("login", views.login),
    path('logout', views.logout),
    path('item/<itemid>',views.item),
    path('addtoCart/<itemid>', views.addtoCart),
    path('cart', views.cart),
    path('sendemail', views.sendemail),
    path('contact', views.contact),
]
