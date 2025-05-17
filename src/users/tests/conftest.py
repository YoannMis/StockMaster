import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def valid_user():
    """
    Fixture to create and return a valid user instance for testing.

    This fixture creates a user with valid credentials and personal information.
    It can be used in tests that require a valid user instance.

    Returns:
        User: A user instance with valid credentials and personal information.
    """
    return User.objects.create_user(
        username="validusername",
        password="validpassword",
        first_name="John",
        last_name="Doe"
    )


@pytest.fixture
def invalid_user():
    """
    Fixture to create and return an invalid user instance for testing.

    This fixture creates a user with invalid credentials but valid personal information.
    It can be used in tests that require an invalid user instance.

    Returns:
        User: A user instance with invalid credentials but valid personal information.
    """
    return User.objects.create_user(
        username="invalidusername",
        password="invalidpassword",
        first_name="John",
        last_name="Doe"
    )


@pytest.fixture
def valid_login():
    """
    Fixture to return valid login credentials for testing.

    This fixture provides a dictionary containing valid login credentials.
    It can be used in tests that require valid login data.

    Returns:
        dict: A dictionary containing valid login credentials.
    """
    valid_login_data = {"username": "validusername",
                        "password": "validpassword",
                        }
    return valid_login_data


@pytest.fixture
def invalid_login():
    """
    Fixture to return invalid login credentials for testing.

    This fixture provides a dictionary containing invalid login credentials.
    It can be used in tests that require invalid login data.

    Returns:
        dict: A dictionary containing invalid login credentials.
    """
    invalid_login_data = {"username": "invalidusername",
                          "password": "invalidpassword",
                          }
    return invalid_login_data
