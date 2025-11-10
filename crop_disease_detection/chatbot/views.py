import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os

# Load key from environment if available
GROQ_API_KEY = "your api key"

@csrf_exempt
def chatbot_view(request):
    """Render chatbot page."""
    return render(request, 'chatbot/chatbot.html')


@csrf_exempt
def chatbot_api(request):
    """Handles AJAX chat requests."""
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        if not user_message.strip():
            return JsonResponse({'response': "Please enter a message."})

        try:
            # Groq API endpoint (using Mixtral model)
            url = "https://api.groq.com/openai/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": "You are an intelligent crop disease assistant chatbot."},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()

            data = response.json()
            bot_reply = data["choices"][0]["message"]["content"]

            return JsonResponse({'response': bot_reply})

        except Exception as e:
            print("Groq Error:", e)
            return JsonResponse({'response': "⚠️ Unable to connect to Groq API. Please try again later."})

    return JsonResponse({'response': "Invalid request."})
