from django.contrib import admin

from .models import Address, Order, Payment, Product, OrderItem, Brand, Category, WishlistItem

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(WishlistItem)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Address)