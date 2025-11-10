from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500',
                'rows': 5,
                'placeholder': 'Enter your feedback here...'
            }),
        }
        labels = {
            'message': 'Your Feedback'
        }
