from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Importing home view from project-level views


urlpatterns = [
    # 🌾 Home page (requires login, handled by @login_required)
    path('', views.home, name='home'),

    # 🧩 Django Admin
    path('admin/', admin.site.urls),

    # 👤 Accounts (login, register, logout)
    path('accounts/', include('accounts.urls')),

    # 🤖 Chatbot module
    path('chatbot/', include('chatbot.urls')),

    # ☀️ Weather module
    path('weather/', include('weather.urls')),

    # 🧠 Prediction module
    path('prediction/', include('prediction.urls')),

    # 💬 Feedback module
    path('feedback/', include('feedback.urls')),

    # 🌿 Disease Info module
    path('info/', include('info.urls')),

    # 🛠️ Admin Dashboard (custom admin UI)
    path('dashboard/', include('admin_dashboard.urls')),
]

# 🖼️ Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
