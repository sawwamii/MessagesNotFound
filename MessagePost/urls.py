from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name='logout')
]
