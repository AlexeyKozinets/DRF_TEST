import logging
from decimal import Decimal

from celery import shared_task

from DeliveryService.utils import usd_to_rub_exchange_rate
from DeliveryService.models import Package


logger = logging.getLogger("main")

@shared_task
def update_delivery_costs():
    """Update packages delivery cost if its none."""
    
    packages = Package.objects.filter(delivery_cost__isnull=True)

    if not packages:
        logger.info("There are no new packages.")
        return None
        
    exchange_rate = usd_to_rub_exchange_rate()
    updated_packages = []

    if not exchange_rate:
        logger.error("There are no exchange rate to calculate delivery cost.")
        return None

    for package in packages:
        package.delivery_cost = (package.weight * Decimal("0.5") + package.price * Decimal("0.01")) * exchange_rate
        updated_packages.append(package)

    if updated_packages:
        Package.objects.bulk_update(updated_packages, ['delivery_cost'])

    logger.info(f"{len(packages)} packages was processed.")