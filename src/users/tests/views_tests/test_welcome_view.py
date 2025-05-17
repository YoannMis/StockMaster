import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.mark.django_db
def test_welcome_view_with_authenticated_user(client: Client, valid_user: User):
    """
    Test the welcome view with an authenticated user.

    This test simulates a logged-in user by setting the session with a valid user ID.
    It then accesses the welcome view and verifies that the response is correct and
    contains the expected welcome message.

    Args:
        client (Client): Django test client for making requests.
        valid_user (User): A fixture providing a valid user instance for testing.

    Asserts:
        - The response status code is 200 (OK).
        - The response content contains the welcome message for the authenticated user.
    """
    # Create a valid user
    user = valid_user

    # Simulate a logged-in user by setting the session
    session = client.session
    session['logged_user_id'] = user.id
    session.save()

    # Access the welcome view
    response = client.get(reverse("welcome-page"))

    # Verify that the response is correct
    assert response.status_code == 200
    # Verify that the welcome message is correct
    assert b'John Doe' in response.content


@pytest.mark.django_db
def test_welcome_view_with_unauthenticated_user(client: Client):
    """
    Test the welcome view with an unauthenticated user.

    This test accesses the welcome view without being logged in and verifies that
    the user is redirected to the login page.

    Args:
        client (Client): Django test client for making requests.

    Asserts:
        - The response status code is 302 (Redirect).
        - The response URL is the login page URL.
    """
    # Access the welcome view without being logged in
    response = client.get(reverse("welcome-page"))
    # Verify that the user is redirected to the login page
    assert response.status_code == 302
    assert response.url == reverse("login-page")
