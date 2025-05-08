from django.core.serializers import serialize
from django.shortcuts import render
from .models import postData
import socket
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from .models import UserProfile
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import CommentForm
from .models import postData, Comment
from django.shortcuts import get_object_or_404, redirect

  

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def index(request):
    ip = get_ip()
    savedPosts = postData.objects.all()
    savedPosts_json = json.loads(serialize('json', savedPosts))
    return render(request, 'MessagePost/index.html', {'title':'MESSAGES_NOT_FOUND', 'ip': ip, 'savedPosts': savedPosts_json})
    posts = postData.objects.all().order_by('-id')
    comment_form = CommentForm()
    return render(request, 'index.html', {
        'posts': posts,
        'comment_form': comment_form,
        'ip': get_client_ip(request),
    })

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user to the database
            messages.success(request, 'Your account has been created! You can now log in.')

            return redirect('login')  # After successful registration, redirect to login
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = UserRegisterForm()

    return render(request, 'MessagePost/register.html', {'form': form})
################ login forms############################################### 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('index')  # Redirect to homepage after login
            else:
                messages.error(request, 'Invalid username or password.')
                print("Authentication failed!")  # Debug if authentication fails
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'MessagePost/login.html', {'form': form})
	
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(postData, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)