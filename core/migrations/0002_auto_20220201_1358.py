# Generated by Django 3.0.3 on 2022-02-01 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcarrousel',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='itemcarrousel',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
