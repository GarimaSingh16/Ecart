# Generated by Django 5.2 on 2025-06-27 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_orderproduct_color_remove_orderproduct_size'),
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
