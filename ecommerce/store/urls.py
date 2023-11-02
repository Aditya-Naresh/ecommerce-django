from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('brand/<slug:brand_slug>/', views.store, name='products_by_brand'),
    path('<slug:brand_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
