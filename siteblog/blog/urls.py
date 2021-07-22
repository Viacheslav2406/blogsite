from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', ViewPost.as_view(), name='post'),
    # path('author/', PostsByAuthor.as_view(), name='author'),
    path('post/add_post/', CreatePost.as_view(), name='add_post'),
    path('post/<str:slug>/update_post/', UpdatePost.as_view(), name='update_post'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),


]
