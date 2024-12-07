from django.urls import path 
from . import views 
 
urlpatterns = [ 
    path('', views.search_view, name='search'), 
    path('search/', views.search_view, name='search'), 
    path('product/new/', views.product_create, name='product_create'), 
    path('product/<int:pk>/', views.product_detail, name='product_detail'), 
    path('product/<int:pk>/edit/',  views.product_update, name='product_update'), 
    path('product/<int:pk>/delete',  views.product_delete, name='product_delete'), 
    path('products/', views.product_list, name='product_list'), 
    path('favorite/toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('cart/', views.cart_list, name='cart_list'),
    path('remove_one_from_cart/<int:product_id>/', views.remove_one_from_cart, name='remove_one_from_cart'),
    path('cart/purchase/', views.purchase_cart, name='purchase_cart'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('manual_restock/', views.manual_restock, name='manual_restock'),
    path('toggle_auto_restock/', views.toggle_auto_restock, name='toggle_auto_restock'),
]
