# Generated by Django 3.2.15 on 2022-10-08 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
        ('users', '0002_mytoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('recipe.shopingcart',),
        ),
    ]