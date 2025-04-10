# product/tests/conftest.py

import os
import django
import pytest

# Set Django settings for tests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()

# Import AFTER setup
from product.tests.test_seed_utils import reseed_test_data

@pytest.fixture(autouse=True, scope="function")
def reseed_before_each_test():
    """Clean and reseed the test DB before each test function."""
    reseed_test_data()
