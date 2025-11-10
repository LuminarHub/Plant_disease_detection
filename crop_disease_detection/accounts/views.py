from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .forms import RegistrationForm, LoginForm

class RegisterView(View):
    """Handles user registration"""
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_farmer = form.cleaned_data.get('is_farmer', False)
            user.save()
            messages.success(request, "✅ Account created successfully! Please login.")
            return redirect('login')
        messages.error(request, "❌ Registration failed. Please correct the errors below.")
        return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Handles login for registered users"""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Welcome {user.username}! 👋")

                # ✅ Redirect based on role
                if hasattr(user, 'is_admin') and (user.is_admin or user.is_superuser):
                    return redirect('admin_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Logs out the user"""
    logout(request)
    messages.info(request, "👋 You have successfully logged out.")
    return redirect('login')
