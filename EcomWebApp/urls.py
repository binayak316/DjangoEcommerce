from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="index"),
    path('detail/<int:pk>/', views.detail, name="detail-page"),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),

    path('update-Item/', views.updateItem, name='update-Item'),
    path('process_order/', views.processOrder, name='process_order'),

]


