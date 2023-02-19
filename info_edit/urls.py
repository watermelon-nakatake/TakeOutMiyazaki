from django.urls import path

from . import views

app_name = 'info_edit'
urlpatterns = [
    # 初期画面
    path('', views.index, name='index'),
    # 現在のレストラン情報を確認するページ
    path('user/top/', views.user_detail, name='user_detail'),
    # レストラン情報を作成
    path('user/create_main/', views.restaurant_create, name='user_create'),
    # レストラン情報を更新
    path('user/edit_main/', views.restaurant_edit, name='user_edit_main'),
    # レストラン用画像のアップロード
    path('user/image_upload/', views.restaurant_image_upload, name='user_image_upload'),

    # メニュー新規作成
    path('user/menu_create/', views.menu_create, name='menu_create', ),
    # メニュー情報の更新
    path('user/menu_edit/<int:menu_pk>/', views.menu_edit, name='menu_edit'),

    # 一般利用者が閲覧するレストラン情報
    path('restaurant/detail/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    # 一般利用者が閲覧するメニュー情報
    path('restaurant/dish/<int:menu_id>/', views.menu_detail, name='restaurant_dish'),

    # クラスビューの練習
    path('user/menu_create2/<int:r_pk>/', views.MenuCreateView.as_view(), name='menu_create2'),
    path('user/menu_update/<int:pk>/', views.MenuUpdateView.as_view(), name='menu_update'),
    path('user/restaurant_create/', views.RestaurantCreateView.as_view(), name='restaurant_create'),
    path('user/restaurant_detail/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),

]
