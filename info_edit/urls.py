from django.urls import path

from . import views

app_name = 'info_edit'
urlpatterns = [
    path('', views.index, name='index'),
    path('user/top/', views.user_detail, name='user_detail'),
    path('user/create_main/', views.restaurant_create, name='user_create'),
    path('user/edit_main/', views.restaurant_edit, name='user_edit_main'),
    path('user/image_upload/', views.restaurant_image_upload, name='user_image_upload'),
    path('user/menu_create/', views.menu_create, name='menu_create', ),
    path('user/menu_edit/<int:restaurant_menu_id>/', views.menu_edit, name='menu_edit'),
    path('restaurant/detail/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/dish/<int:menu_id>/', views.menu_detail, name='restaurant_dish'),

    path('user/menu_input/<int:pk>/', views.MenuInputView.as_view(), name='menu_input'),
    path('user/restaurant_detail/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant_detail'),

]
