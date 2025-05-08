"""
URL configuration for MessagesNotFound project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.urls import path # Redundant import, removed
from django.contrib.auth import views as auth_views # Renamed for clarity
from MessagePost import views as user_view

# For serving media files during development
from django.conf import settings # <--- ADD THIS LINE
from django.conf.urls.static import static # <--- ADD THIS LINE

urlpatterns = [
    path('', include('MessagePost.urls')), # This includes your app's URLs
    path('admin/', admin.site.urls),
    # path('admin/', admin.site.urls), # Duplicate admin path, removed one
    
    # These login/logout/register URLs seem to be duplicates of what might be in MessagePost.urls
    # If they are defined in MessagePost.urls, you might not need them here.
    # However, your views.py for MessagePost has `login_view` (not `login`)
    # and register. Let's assume they are meant to be here for now.
    # path('login/', user_view.login, name ='login'), # Your view is login_view
    path('login/', user_view.login_view, name ='login'), # <--- CORRECTED if using the view from MessagePost.views
    path('logout/', auth_views.LogoutView.as_view(template_name ='MessagePost/index.html'), name ='logout'),
    path('register/', user_view.register, name ='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)