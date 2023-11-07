from django.urls import path
from . import views
urlpatterns = [
    path('', views.useradmin, name='useradmin'),
    path('unauthorized/', views.decorator, name='decorator'),

#===========================Users==================================
# Customers----------------------------------------------------------------------------------------------------
    path('customers/', views.customers, name='customers'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),

#Admin-------------------------------------------------------------------------------------------------------- 
    path('admin_list/', views.admin_list, name='admin_list' ),
    path('delete_admin/<int:user_id>/', views.delete_admin, name='delete_admin'),
    path('create_admin/', views.create_admin, name='create_admin'),

# Categories----------------------------------------------------------------------------------------------------
    path('categories/', views.categories, name='categories'),
    path('edit_category/<int:cat_id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:cat_id>', views.delete_category, name='delete_category'),
    path('add_category', views.add_category, name='add_category'),

# Brands-------------------------------------------------------------------------------------------------------------
    path('brands/', views.brands, name='brands'),
    path('edit_brand/<int:brand_id>', views.edit_brand, name='edit_brand'),
    path('delete_brand/<int:brand_id>', views.delete_brand, name='delete_brand'),
    path('add_brand', views.add_brand, name='add_brand'),
]
