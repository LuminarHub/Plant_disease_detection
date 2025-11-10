from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    """
    Main home/dashboard page for logged-in users.
    - Redirects admin users to the admin dashboard.
    - Shows home.html (dashboard) for normal users.
    - Forces login for guests.
    """
    # ✅ If the user is an admin, redirect to custom dashboard
    if hasattr(request.user, 'is_admin') and request.user.is_admin:
        return redirect('admin_dashboard')

    # ✅ Otherwise show the standard user home page
    return render(request, 'home.html')
