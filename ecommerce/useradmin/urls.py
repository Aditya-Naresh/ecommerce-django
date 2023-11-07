from django.urls import path
from . import views
urlpatterns = [
    path('', views.useradmin, name='useradmin'),
    path('unauthorized', views.decorator, name='decorator'),

#===========================Users==================================
# Customers----------------------------------------------------------------------------------------------------
    path('customers', views.customers, name='customers'),
    path('block_user/<int:user_id>', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>', views.unblock_user, name='unblock_user'),

#Admin-------------------------------------------------------------------------------------------------------- 
    path('admin_list', views.admin_list, name='admin_list' ),
    path('delete_admin/<int:user_id>', views.delete_admin, name='delete_admin'),
    path('create_admin', views.create_admin, name='create_admin')
]
