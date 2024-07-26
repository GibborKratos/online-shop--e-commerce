from django.urls import path
from .views import Home, ProductDetail, Wallet, OrderHistory, CartView, BargainView, VendorBargain, delete_bargain, verify_payment, Profile, MyShop, add_product, category, deliveries, deliver, receive, search, delete_cart_item

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("my_shop/", MyShop.as_view(), name="my_shop"),
    path('search/', search, name='search'),
    path("cart/", CartView.as_view(), name="cart"),
    path('category/<str:category>', category , name="category"),
    path("profile/", Profile.as_view(), name="profile"),
    path("bargains/", BargainView.as_view(), name="bargains"),
    path("my_shop/bargains/", VendorBargain.as_view(), name="seller_bargains"),
    path("delete_bargain/<int:id>", delete_bargain, name="delete_bargain"),
    path('product_detail/<slug:id>/', ProductDetail.as_view(), name='product_detail'),
    path('wallet/', Wallet.as_view(), name='wallet'),
    path("order_history/", OrderHistory.as_view(), name="order_history"),
    path('verify_payment/<str:ref>', verify_payment, name="verify_payment"),
    path('my_shop/add_product/', add_product, name="add_product"),
    path("my_shop/deliveries/", deliveries , name="deliveries"),
    path("deliver/<int:id>", deliver, name="deliver"),
    path("delete_cart_item/<int:id>", delete_cart_item, name="delete_cart_item"),
    path("receive/<int:id>", receive, name="receive"),
]
