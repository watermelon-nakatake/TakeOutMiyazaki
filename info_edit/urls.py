from django.urls import path

from . import views

app_name = 'info_edit'
urlpatterns = [
    path('', views.index, name='index'),
    path('user/top', views.Top.as_view(), name='user_top'),
    path('user/create_main', views.restaurant_create, name='user_create'),
    path('user/detail/', views.user_detail, name='user_detail'),
    path('user/edit_main/', views.restaurant_edit, name='user_edit_main'),
    path('user/image_upload/', views.restaurant_image_upload, name='user_image_upload'),
    path('restaurant/detail/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/dish/<int:menu_id>/', views.menu_detail, name='restaurant_dish'),
]
