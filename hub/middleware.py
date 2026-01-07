from django.shortcuts import redirect
from django.contrib import messages

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not request.path.startswith('/admin/login'):
            if request.user.is_authenticated:
                full_name = f"{request.user.first_name} {request.user.last_name}".strip()
                if not (full_name == "Jonalyn Rosell" or request.user.username == "jona" or request.user.is_superuser):
                    messages.error(request, "Access denied. Only Jonalyn Rosell can access the admin panel.")
                    return redirect('dashboard')
            
        response = self.get_response(request)
        return response
