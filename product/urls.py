from django.urls import path

from .views import CategoryView, HandleProduct, HandleProductP, CartTotal, CartDetail, Checkout,CartDetailM, Wishlist, WishlistQ

product_patterns = ([
    path('product/', HandleProduct.as_view()),
    path('category/', CategoryView.as_view()),
    path("product/<int:pk>", HandleProductP.as_view()),
    path("cart/", CartTotal.as_view()),
    path("cart-detail/", CartDetail.as_view()),
    path("cart-detail/<int:pk>", CartDetailM.as_view()),
    path("checkout/", Checkout.as_view()),
    path("wishlist/", Wishlist.as_view()),
    path("wishlist/<int:pk>", WishlistQ.as_view()),
], 'product')