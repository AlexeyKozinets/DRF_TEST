# Generated by Django 5.0.6 on 2024-06-12 16:44

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DeliveryService', '0002_alter_package_session_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='packagecategory',
            options={'ordering': ['name'], 'verbose_name': 'Package Category', 'verbose_name_plural': 'Package Categories'},
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='USD', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='package',
            name='weight',
            field=models.DecimalField(decimal_places=2, help_text='Kg', max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]
