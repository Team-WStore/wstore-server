from django.contrib import admin

from .models import Order, Product, OrderItem, ImageProductItem

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ImageProductItem)