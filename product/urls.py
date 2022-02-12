from django.urls import path

from .views import BrandUpdateDelete, BrandView, CategoryCreate, CategoryDelete, CategoryUpdate, CategoryView, HandleProduct, HandleProductP, CartTotal, CartDetail, CartDetailM, ItemProductCreate, OrderDetail, OrderView, PaymentView, Wishlist, WishlistQ, ProductDetail

product_patterns = ([
    path('product/', HandleProduct.as_view()),
    path("product-create/", ItemProductCreate.as_view()),
    path('category/', CategoryView.as_view()),
    path('category-create/', CategoryCreate.as_view()),
    path('category-modify/<int:pk>', CategoryDelete.as_view()),
    path('category-update/', CategoryUpdate.as_view()),
    path('brand/', BrandView.as_view()),
    path('brand-modify/<int:pk>', BrandUpdateDelete.as_view()),
    path("product/<int:pk>", HandleProductP.as_view()),
    path("product-detail/<slug:slug>", ProductDetail.as_view()),
    path("cart/", CartTotal.as_view()),
    path("cart-detail/", CartDetail.as_view()),
    path("cart-detail/<int:pk>", CartDetailM.as_view()),
    path("wishlist/", Wishlist.as_view()),
    path("wishlist/<int:pk>", WishlistQ.as_view()),
    path("payment/", PaymentView.as_view()),
    path("order/", OrderView.as_view()),
    path("order-detail/", OrderDetail.as_view()),
], 'product')
