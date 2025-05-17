from django.http import HttpResponseRedirect
from django.contrib.auth import get_user, authenticate, login, get_user_model
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm

User = get_user_model()


# def get_logged_user_id(request):
#     logged_user = get_user(request)
#     print(f"user = {logged_user}")
#     if logged_user.is_authenticated:
#         logged_user_id = logged_user.id
#
#     return logged_user_id


def welcome_view(request):
    """
    Display a welcome message to the logged-in user or redirect to the login page if not logged in.

    This view checks if the user is logged in by verifying the presence of 'logged_user_id' in the session.
    If the user is logged in, it retrieves the user's first and last name and renders a welcome page.
    If the user is not logged in, it redirects to the login page.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: A rendered welcome page if the user is logged in, otherwise a redirect to the login page.
    """
    # Check if the user is logged in by verifying the presence of 'logged_user_id' in the session
    if "logged_user_id" in request.session:
        # Retrieve the logged-in user's ID from the session
        logged_user_id = request.session["logged_user_id"]
        # Get the logged-in user's object from the database
        logged_user = User.objects.get(id=logged_user_id)
        # Extract the first and last name of the logged-in user
        first_name = logged_user.first_name
        last_name = logged_user.last_name
        # Combine the first and last name into a full name
        name = f"{first_name} {last_name}"
        # Render the welcome page with the user's full name
        return render(request, "users/index.html", {"name": name})

    # Or redirect to the login page if the user is not logged in
    return HttpResponseRedirect(reverse("login-page"))


def login_view(request):
    """
    Handle user login by authenticating the user and redirecting to the welcome page if successful.

    This view processes a login form submission. If the form is valid, it attempts to authenticate
    the user with the provided username and password. If authentication is successful, the user
    is logged in, and their user ID is stored in the session. The user is then redirected to the
    welcome page. If authentication fails, an error message is displayed.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: A rendered login page if the request method is GET or if authentication fails,
                      otherwise a redirect to the welcome page.
    """
    # Check if the request method is POST
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = LoginForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Extract the username and password from the form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            # Check if authentication was successful
            if user is not None:
                # Log the user in
                login(request, user)
                # Store the user's ID in the session
                request.session["logged_user_id"] = user.id
                # Redirect to the welcome page
                return HttpResponseRedirect(reverse("welcome-page"))
            else:
                # Display an error message if authentication fails
                messages.error(request, message="Username or password invalid")
    else:
        # Create an empty form instance if the request method is GET
        form = LoginForm()

    # Render the login page with the form
    return render(request, "users/login.html", {"form": form})

