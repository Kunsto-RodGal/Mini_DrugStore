from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # This is the new way to define a view in Django 3.0
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('users/', views.UserListView.as_view()),
]


router = DefaultRouter()
router.register('orders', views.OrderViewSet)

urlpatterns += router.urls
