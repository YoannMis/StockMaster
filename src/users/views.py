from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(redirect_field_name=None)
def welcome_view(request):
    """
    Render the welcome page for authenticated users.
    This view is decorated with the `login_required` decorator, which ensures that only authenticated
    users can access it. If the user is not authenticated, they will be redirected to the login page.
    Args:
        request (HttpRequest): The request object containing metadata about the request.
    Returns:
        HttpResponse: A rendered welcome page for authenticated users.
    """
    return render(request, template_name="users/index.html")
