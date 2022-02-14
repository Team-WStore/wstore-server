# Generated by Django 3.0.3 on 2022-02-09 17:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20220206_1721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date_ordered']},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='being_delivered',
            new_name='reviewed',
        ),
        migrations.RemoveField(
            model_name='order',
            name='start_date',
        ),
        migrations.AddField(
            model_name='order',
            name='delivered_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='reviewed_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='sent_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]