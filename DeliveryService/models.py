from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator


class PackageCategory(models.Model):
    name = models.CharField(max_length=125)

    class Meta:
        verbose_name = 'Package Category'
        verbose_name_plural = 'Package Categories'
        ordering = ['name',]

    def __str__(self):
        return self.name


class Package(models.Model):

    category = models.ForeignKey("PackageCategory", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=5, 
                                 decimal_places=2, 
                                 validators=[MinValueValidator(Decimal(0.0)),],
                                 help_text="Weight of content in Kg")
    price = models.DecimalField(max_digits=10, 
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal(0.0)),],
                                help_text="Price of content in USD.")
    delivery_cost = models.DecimalField(max_digits=10, 
                                        decimal_places=2,
                                        validators=[MinValueValidator(Decimal(0.0)),],
                                        null=True, blank=True, default=None,
                                        help_text="Cost of delivery in USD") # db_index=True, 
    
    session_id = models.CharField(max_length=40, null=True, blank=True,)  # db_index=True, 

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Package'

    def __str__(self):
        return self.name


