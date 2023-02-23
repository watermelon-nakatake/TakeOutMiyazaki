from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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


    # メニュー新規作成
    path('user/menu_create/', views.menu_create, name='menu_create', ),
    # メニュー情報の更新
    path('user/menu_edit/<int:menu_pk>/', views.menu_edit, name='menu_edit'),

    # 一般利用者が閲覧するレストラン情報
    path('restaurant/detail/<int:restaurant_pk>/', views.restaurant_detail, name='restaurant_detail'),
    # 一般利用者が閲覧するメニュー情報
    path('restaurant/dish/<int:menu_pk>/', views.menu_detail, name='restaurant_dish'),

    # クラスビューで実装
    # 店舗 create
    path('user/restaurant_create/', views.RestaurantCreateView.as_view(), name='restaurant_create'),
    # 店舗 read
    path('user/restaurant_detail/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail_u'),
    # 店舗 update
    path('user/restaurant_update/<int:pk>/', views.RestaurantUpdateView.as_view(), name='restaurant_update'),
    # 店舗 delete
    path('user/restaurant_delete/<int:pk>/', views.RestaurantDeleteView.as_view(), name='restaurant_delete'),

    # メニュー create
    path('user/menu_create2/<int:r_pk>/', views.MenuCreateView.as_view(), name='menu_create2'),
    # メニュー read
    path('user/menu_detail/<int:pk>/', views.MenuDetailView.as_view(), name='menu_detail'),
    # メニュー update
    path('user/menu_update/<int:pk>/', views.MenuUpdateView.as_view(), name='menu_update'),
    # メニュー delete
    path('user/menu_delete/<int:pk>/', views.MenuDeleteView.as_view(), name='menu_delete'),

    # 店舗画像アップロード
    path('user/image_upload/', views.RestaurantImageUploadView.as_view(), name='user_image_upload'),
    # 店舗画像削除
    path('user/image_delete/<int:pk>/', views.RestaurantImageDeleteView.as_view(), name='user_image_delete'),
    # 料理画像アップロード
    path('user/menu_image_upload/<int:menu_pk>/', views.MenuImageUploadView.as_view(), name='menu_image_upload'),
    # 料理画像削除
    path('user/menu_image_delete/<int:pk>/', views.MenuImageDeleteView.as_view(), name='menu_image_delete'),


    path('restaurant_data/list/', views.ExRestaurantListView.as_view(), name='ex_restaurant_list'),
    path('restaurant_data/detail/<int:pk>/', views.ExRestaurantDetailView.as_view(), name='ex_restaurant_detail'),
    path('restaurant_data/menu/<int:pk>/', views.ExMenuDetailView.as_view(), name='ex_menu_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
