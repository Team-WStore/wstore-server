from django.urls import path

from .views import CategoryView, HandleProduct, HandleProductP, CartTotal, CartDetail, CartDetailM, PaymentView, Wishlist, WishlistQ, ProductDetail

product_patterns = ([
    path('product/', HandleProduct.as_view()),
    path('category/', CategoryView.as_view()),
    path("product/<int:pk>", HandleProductP.as_view()),
    path("product-detail/<slug:slug>", ProductDetail.as_view()),
    path("cart/", CartTotal.as_view()),
    path("cart-detail/", CartDetail.as_view()),
    path("cart-detail/<int:pk>", CartDetailM.as_view()),
    path("wishlist/", Wishlist.as_view()),
    path("wishlist/<int:pk>", WishlistQ.as_view()),
    path("payment/", PaymentView.as_view()),
], 'product')
