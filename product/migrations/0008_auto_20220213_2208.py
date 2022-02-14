# Generated by Django 3.0.3 on 2022-02-14 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='reviewed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='sent_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]