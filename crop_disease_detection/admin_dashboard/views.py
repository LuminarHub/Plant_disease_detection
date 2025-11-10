from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import CustUser
from feedback.models import Feedback
from prediction.models import History  # Ensure this model exists
from django.utils import timezone

# ✅ Custom decorator for admin-only access
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # ✅ Allow both custom admins and Django superusers
        if not (request.user.is_admin or request.user.is_superuser):
            messages.error(request, "Access denied. Admins only.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='login')
@admin_required
def admin_dashboard(request):
    """Admin Dashboard with stats and recent data"""
    total_users = CustUser.objects.count()
    total_predictions = History.objects.count() if History.objects.exists() else 0
    total_feedbacks = Feedback.objects.count()

    recent_predictions = History.objects.all().order_by('-created_at')[:5]
    recent_feedbacks = Feedback.objects.all().order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'total_predictions': total_predictions,
        'total_feedbacks': total_feedbacks,
        'recent_predictions': recent_predictions,
        'recent_feedbacks': recent_feedbacks,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


@login_required(login_url='login')
@admin_required
def users_list(request):
    """Display all registered users"""
    users = CustUser.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard/users.html', {'users': users})


@login_required(login_url='login')
@admin_required
def feedbacks_list(request):
    """Display all user feedbacks"""
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/feedbacks.html', {'feedbacks': feedbacks})
