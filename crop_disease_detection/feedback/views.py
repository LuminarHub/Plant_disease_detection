from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from .models import Feedback

@login_required
def feedback_view(request):
    """Handles user feedback submission."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('feedback_page')
    else:
        form = FeedbackForm()

    user_feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'feedback/feedback.html', {'form': form, 'feedbacks': user_feedbacks})
