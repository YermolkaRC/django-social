from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'social'
urlpatterns = [
    path('', views.index, name='index'),
    #Add path for API calls ???
    #path('users/', include('django.contrib.auth.urls')),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('users/<username>/posts/', views.user_posts, name='user_posts'),
    path('users/<username>/create_post/', views.creaete_post, name='create_post'),
    path('posts/<int:postid>/', views.post_detail, name='post_detail'),
    path('register/', views.user_create, name='user_create'),
    #path('login/', views.user_login, name='user_login'),
    path('login/', views.ViewLogin.as_view(), name='user_login'),
    path('logout/', views.LogoutView.as_view(), name='user_logout'),
    path('users/<username>/new_post', views.creaete_post, name='post_create'),
]