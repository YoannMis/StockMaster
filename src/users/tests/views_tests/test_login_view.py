import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from pytest_django.asserts import assertTemplateUsed
from django.contrib.messages import get_messages

from users.tests.conftest import valid_login, invalid_login

User = get_user_model()


@pytest.mark.django_db
def test_login_view_with_valid_credentials(client: Client, valid_user: User, valid_login: dict):
    """
    Test the login view with valid user credentials.

    This test creates a valid user and attempts to log in with valid credentials.
    It verifies that the user is redirected to the welcome page and that the user
    is successfully logged in.

    Args:
        client (Client): Django test client for making requests.
        valid_user (User): A fixture providing a valid user instance for testing.
        valid_login (dict): A fixture providing valid login credentials.

    Asserts:
        - The response status code is 302 (Redirect).
        - The response URL is the welcome page URL.
        - The user is logged in (session contains "_auth_user_id").
    """
    # Access to the login view with valid user credentials
    response = client.post(reverse("users:login-page"), data=valid_login)

    # Verify that the user is redirected to the welcome page
    assert response.status_code == 302
    assert response.url == reverse("welcome-page")
    # Verify that the user is connected
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_login_view_with_invalid_credentials(client: Client, valid_user: User, invalid_login: dict):
    """
    Test the login view with invalid user credentials.

    This test attempts to log in with invalid credentials and verifies that the
    user is not redirected to the welcome page, not logged in, and that an error
    message is displayed.

    Args:
        client (Client): Django test client for making requests.
        invalid_login (dict): A fixture providing invalid login credentials.

    Asserts:
        - The response status code is 200 (OK).
        - The user is not logged in (session does not contain "_auth_user_id").
        - An error message is displayed indicating invalid username or password.
    """
    # Access to the login view with invalid user credentials
    response = client.post(reverse("users:login-page"), data=invalid_login)

    # Verify that the user is not redirected to the welcome page
    assert response.status_code == 200

    # Verify that the user is not connected
    assert "_auth_user_id" not in client.session

    # Verify that an error message is displayed


def test_login_view_get_request(client: Client):
    """
    Test the login view with a GET request.

    This test accesses the login view with a GET request and verifies that the
    response is correct, the correct template is used, and the login form is displayed.

    Args:
        client (Client): Django test client for making requests.

    Asserts:
        - The response status code is 200 (OK).
        - The correct template ("users/login.html") is used.
        - The login form fields ("username" and "password") are present in the response content.
    """
    # Access to the login view with a GET request
    response = client.get(reverse("users:login-page"))

    # Verify that the response is correct
    assert response.status_code == 200

    # Verify that the good template is used
    assertTemplateUsed(response, "users/login.html")

    # Verify that the login form is displayed
    assert b"username" in response.content
    assert b"password" in response.content
