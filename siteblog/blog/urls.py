from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', ViewPost.as_view(), name='post'),
    path('author/', MyPosts.as_view(), name='author'),
    path('add_post/', CreatePost.as_view(), name='add_post'),
    path('post/<str:slug>/update_post/', UpdatePost.as_view(), name='update_post'),
    path('post/<str:slug>/delete_post/', DeletePost.as_view(), name='delete_post'),
    path('post/<str:slug>/comment/<int:pk>/delete_comment', DeleteComment.as_view(), name='delete_comment'),
    path('post/<str:slug>/send_post', send_post_to_email, name='send_post'),
    path('popular_posts/', get_popular_posts, name='popular_posts'),
    path('add_tag/', CreateTag.as_view(), name='add_tag'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('search/', Search.as_view(), name='search')

]
