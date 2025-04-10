from django.apps import AppConfig
from django.db.utils import OperationalError
from mongoengine.errors import NotUniqueError
from django.core.exceptions import ImproperlyConfigured
import logging

logger = logging.getLogger(__name__)

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        import sys

        # Don't run seed logic during test collection or test execution
        if any(arg in sys.argv[0] for arg in ["pytest", "test"]):
            return

        from .seed_utils import seed_categories, seed_legacy_products

        try:
            seed_categories()
            seed_legacy_products()
        except (OperationalError, ImproperlyConfigured, NotUniqueError) as e:
            logger.error(f"error during seeding: {e}")

