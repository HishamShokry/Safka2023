from django.shortcuts import redirect

class RoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Check user role and redirect accordingly
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return response  # Superusers go to the default view
            elif request.user.is_vendor:
                return redirect('vendor_dashboard')  # Redirect staff to vendor/dashboard
            elif request.user.is_marketer:
                return redirect('marketer_dashboard')  

        return response
    
    