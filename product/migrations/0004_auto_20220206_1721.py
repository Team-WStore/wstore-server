# Generated by Django 3.0.3 on 2022-02-06 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20220206_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ordered_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Address'),
        ),
    ]