# Generated by Django 3.0.3 on 2022-02-12 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_order_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=7, verbose_name='Total'),
        ),
    ]
