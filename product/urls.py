from django.urls import path

from .views import HandleProduct, HandleProductP, CartTotal, CartDetail, Checkout,CartDetailM

product_patterns = ([
    path('product/', HandleProduct.as_view()),
    path("product/<int:pk>", HandleProductP.as_view()),
    path("cart/", CartTotal.as_view()),
    path("cart-detail/", CartDetail.as_view()),
    path("cart-detail/<int:pk>", CartDetailM.as_view()),
    path("checkout/", Checkout.as_view()),

], 'product')