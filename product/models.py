from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from slugify import slugify

import random
import string


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear'),
    ('AC', 'Accesories'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
# Create your models here.

class ImageProductItem(models.Model):
    image = models.URLField(max_length=200, null=True, blank= True)
    def __str__(self):
        return self.image


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Precio con descuento'
    )
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=2, verbose_name='Categoría')
    images = models.ManyToManyField(ImageProductItem)
    slug = models.SlugField(verbose_name='Nombre Slug',
                            unique=True, null=True, blank=True)

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
        total = self.product.price * self.quantity
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


class Order(models.Model):
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    @property
    def get_total(self):
        orderitems = self.items.all()
        total = sum([item.get_total for item in orderitems])
        if self.coupon:
            total -= self.coupon.amount
        return total

    @property
    def get_cart_items(self):
        orderitems = self.products.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return self.user.username + ' ---Date--- ' + str(self.start_date)

    def save(self, *args, **kwargs):
        self.ref_code = create_ref_code()
        super(Order, self).save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Direcciones'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


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
