# Generated by Django 5.0.6 on 2024-06-12 17:01

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DeliveryService', '0003_alter_packagecategory_options_alter_package_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='delivery_cost',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Cost of delivery in USD', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10, help_text='Price of content in USD.', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='package',
            name='weight',
            field=models.DecimalField(decimal_places=2, help_text='Weight of content in Kg', max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]
