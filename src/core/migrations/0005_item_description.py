# Generated by Django 3.0.5 on 2020-05-03 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='this is a test description'),
            preserve_default=False,
        ),
    ]
