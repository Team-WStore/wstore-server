from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from slugify import slugify

from core.models import ImageItem

import random
import string

""" ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
) """

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nombre')
    image = models.ForeignKey(
        ImageItem, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name        

class Brand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='Precio')
    discount = models.PositiveIntegerField(null=True, blank=True)
    discount_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Precio con descuento'
    )
    category = models.ForeignKey(
        Category, verbose_name='Categoría', on_delete=models.CASCADE)
    images = models.ManyToManyField(ImageItem, verbose_name='Imágenes')
    slug = models.SlugField(verbose_name='Nombre Slug',
                            unique=True, null=True, blank=True)
    available = models.PositiveIntegerField(verbose_name='Disponibilidad', default=0)
    description = models.TextField(verbose_name='Descripción')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.discount_price = float(self.price) * (1 - (self.discount/100))
        super(Product, self).save(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def get_amount_saved(self):
        return self.get_total() - self.get_total_discount_item_price()

    @property
    def get_total(self):
        total = self.product.discount_price * self.quantity + 1
        return total

    @property
    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    @property
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def __str__(self):
        return "{} of {} -- {}".format(self.quantity, self.product.name, self.user.username)

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "{} -- {}".format(self.product.name, self.user.username)


class Order(models.Model):
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(OrderItem)


    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, blank=True, null=True)

    """ billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True) """
        
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    """ coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True) """

    date_ordered = models.DateTimeField(auto_now_add=True)

    reviewed_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    reviewed = models.BooleanField(default=False)

    sent_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    sent = models.BooleanField(default=False)

    delivered_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    delivered = models.BooleanField(default=False)
    
    received = models.BooleanField(default=False)

    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    total = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='Total', default='0.00')

    class Meta:
        ordering = ['-date_ordered']

    @property
    def get_total(self):
        orderitems = self.products.all()
        return sum([item.get_total for item in orderitems])

    @property
    def get_cart_items(self):
        orderitems = self.products.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return self.user.username + ' ---Date--- ' + str(self.date_ordered)

    def save(self, *args, **kwargs):
        self.ref_code = create_ref_code()
        super(Order, self).save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    # country = models.CharField(max_length=50)
    zip = models.CharField(max_length=100)
    # address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    # default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Direcciones'


class Payment(models.Model):
    charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.charge_id


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return str(self.pk)
