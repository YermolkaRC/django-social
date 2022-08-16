from math import hypot
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth import views as auth_views
from django.utils import timezone

from .models import Post, User, create_user

# Create your views here.

def index(request):
    latest_posts = Post.objects.order_by('-date_created')[:5]
    user = User.objects.get(username=request.user.username) if request.user.is_authenticated else None

    context = {
        'latest_posts': latest_posts,
        'is_authenticated': request.user.is_authenticated,
        'user': user,
    }
    return render(request, 'social/index.html', context)

def user_detail(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'social/user/not_found.html', {})    
    return render(request, 'social/user/detail.html', {'user': user})

def user_posts(request, username):
    user = User.objects.get(username=username) if request.user.is_authenticated else None

    context = {
        'is_authenticated': request.user.is_authenticated,
        'username': username,
        'user': user,
    }
    print(user)
    return render(request, 'social/user/posts.html', context)

def user_create(request):
    try:
        request.POST['username'] == ''
    except:
        return render(request, 'social/user/create.html')
    
    username = request.POST['username']
    password = request.POST['password']
    name = request.POST['name']

    if len(username) < 3 or len(password) < 8:
        return render(request, 'social/user/create.html', {'error_message': 'Username should be atleast 4 symbols long'})

    u = create_user(username=username, password=password, name=name)
    if not u:
        return render(request, 'social/user/create.html', {'error_message': 'Username is already taken'})

    
    return HttpResponseRedirect(reverse('social:user_detail', args=(u,)))

def user_login(request):
    try:
        request.GET['username'] == ''
    except:
        return render(request, 'social/user/login.html')
    
    username = request.GET['username']
    password = request.GET['password']
    """try:
        user = User.objects.get(username=username)
    except:
        return render(request, 'social/user/login.html', {'error_message': 'Invalid username'})
    
    if User.check_password(user.username, password):
        """
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        print('logged in')
        return HttpResponseRedirect(reverse('social:index'))
    else:
        return render(request, 'social/user/login.html')
 
def creaete_post(request, username):
    user = User.objects.get(username=request.user.username) if request.user.is_authenticated else None

    context = {
        'is_authenticated': request.user.is_authenticated,
        'user': user,
    }
    
    
    if user is None:
        print('user in none')
        return render(request, 'social/post/create.html', context)

    try:
        name = request.POST['name']
        text = request.POST['text']
    except:
        print('cant fetch data')
        return render(request, 'social/post/create.html', context)
    time = timezone.now()

    post = Post(name=name, text=text, user=user, date_created=time)
    post.save()
    return HttpResponseRedirect(reverse('social:post_detail', args=(post.id, )))

def post_detail(request, postid):
    try:
        post = Post.objects.get(pk=postid)
    except Post.DoesNotExist:
        return render(request, 'social/post/not_found.html')
    return render(request, 'social/post/detail.html', {'post': post})

class ViewLogin(auth_views.LoginView):
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    pass
