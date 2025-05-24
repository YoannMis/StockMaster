from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# def get_logged_user_id(request):
#     logged_user = get_user(request)
#     print(f"user = {logged_user}")
#     if logged_user.is_authenticated:
#         logged_user_id = logged_user.id
#
#     return logged_user_id


@login_required
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
    # user = request.user
    # name = user.first_name
    # Dans le template on peut directement utiliser {{ user }} sans avoir besoin de le passer dans le context
    return render(request, "users/index.html")

