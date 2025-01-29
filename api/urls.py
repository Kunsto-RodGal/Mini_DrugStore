from django.urls import path
from . import views

urlpatterns = [
    # This is the new way to define a view in Django 3.0
    path('products/', views.ProductListAPIView.as_view()),
    path('products/info', views.product_info),
    path('products/<int:product_id>', views.ProductDetailAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
]
