from django.shortcuts import redirect
from django.contrib import messages

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if request.user.is_authenticated:
                full_name = f"{request.user.first_name} {request.user.last_name}".strip()
                # Allow access if user is Jonalyn Rosell, username is jonalynrosell, or is superuser
                if not (full_name == "Jonalyn Rosell" or request.user.username == "jonalynrosell" or request.user.is_superuser):
                    messages.error(request, "Access denied. Only Jonalyn Rosell can access the admin panel.")
                    return redirect('dashboard')
            
        response = self.get_response(request)
        return response
