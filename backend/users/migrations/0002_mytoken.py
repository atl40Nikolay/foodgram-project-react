# Generated by Django 3.2.15 on 2022-10-04 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyToken',
            fields=[
            ],
            options={
                'verbose_name': 'токен',
                'verbose_name_plural': 'токены',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('authtoken.token',),
        ),
    ]
