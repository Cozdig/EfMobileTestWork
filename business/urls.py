from django.urls import path
from .views import ProductListView, ProductCreateView, ProductDetailView

app_name = 'business'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
]