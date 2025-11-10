import os
from django.shortcuts import render
from groq import Groq

# ✅ Initialize Groq client (use your key from environment variable for safety)
client = Groq(api_key=os.environ.get("GROQ_API_KEY") or "your api key")

def disease_info_view(request):
    """Fetch crop disease information dynamically using Groq."""
    query = request.GET.get('q', '').strip()
    ai_response = None
    structured_output = None

    if query:
        try:
            print(f"🧠 Fetching Groq AI data for: {query}")

            prompt = f"""
            Provide detailed agricultural information about '{query}'.
            Include the following in clear sections:
            1. Crop Name
            2. Symptoms
            3. Prevention
            4. Treatment
            Format the response clearly and concisely.
            """

            # ✅ Use the current, supported model
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )

            ai_response = response.choices[0].message.content.strip() if response.choices else None
            print("🧩 Groq raw response:", ai_response)

            # ✅ Handle empty or unexpected AI responses
            if not ai_response:
                ai_response = "⚠️ Groq did not return any information. Please try again later."

            # Attempt to split AI response into structured sections
            structured_output = parse_ai_response(ai_response)

        except Exception as e:
            ai_response = f"⚠️ Error fetching data from Groq API: {e}"
            print(ai_response)

    context = {
        'query': query,
        'ai_response': ai_response,
        'structured_output': structured_output
    }
    return render(request, 'info/disease_info.html', context)


def parse_ai_response(ai_text):
    """Parse AI response into structured sections (Crop, Symptoms, Prevention, Treatment)."""
    if not ai_text:
        return None

    sections = {
        "Crop": "",
        "Symptoms": "",
        "Prevention": "",
        "Treatment": ""
    }

    current_key = None
    for line in ai_text.splitlines():
        line = line.strip()
        if line.lower().startswith("crop"):
            current_key = "Crop"
        elif line.lower().startswith("symptom"):
            current_key = "Symptoms"
        elif line.lower().startswith("prevention"):
            current_key = "Prevention"
        elif line.lower().startswith("treatment"):
            current_key = "Treatment"
        elif current_key:
            sections[current_key] += line + "\n"

    return sections
