# Generated by Django 3.0.3 on 2022-01-26 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCarrousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.URLField(max_length=500)),
                ('url', models.CharField(max_length=200)),
                ('created', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
