import os

import pytest
from django.db import connection


@pytest.mark.django_db
def test_django_connects_to_a_dedicated_postgresql_test_database() -> None:
    developer_database = os.environ.get(
        "DATABASE_NAME", "appointment_booking_development"
    )
    expected_test_database = os.environ.get(
        "DATABASE_TEST_NAME", "appointment_booking_test"
    )

    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database(), 1")
        result = cursor.fetchone()

    assert connection.vendor == "postgresql"
    assert result == (expected_test_database, 1)
    assert result[0] != developer_database
