# Generated by Django 3.2.15 on 2022-10-08 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_shoppingcart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'корзина для покупок', 'verbose_name_plural': 'корзины для покупок'},
        ),
    ]
