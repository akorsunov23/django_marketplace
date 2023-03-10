# Generated by Django 4.1.5 on 2023-02-11 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_shop_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='product_count',
        ),
        migrations.AddField(
            model_name='product',
            name='product_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='product',
            name='shop',
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ManyToManyField(to='marketplace.shop'),
        ),
    ]
