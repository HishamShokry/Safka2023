from django.shortcuts import redirect

def vendor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_vendor or request.user.is_superuser or request.user.is_impersonate):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('signin')  # Redirect to the login page if the user is not a vendor, superuser, or impersonating
    return _wrapped_view

def marketer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_marketer or request.user.is_superuser or request.user.is_impersonate):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('signin')  # Redirect to the login page if the user is not a marketer, superuser, or impersonating
    return _wrapped_view

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser or request.user.is_impersonate):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('signin')  # Redirect to the login page if the user is not an admin, superuser, or impersonating
    return _wrapped_view
