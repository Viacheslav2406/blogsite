from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('/category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('/tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('/post/<str:slug>/', ViewPost.as_view(), name='post'),
    path('/author/<str:slug>/', PostsByAuthor.as_view(), name='author'),
    # path('post/add_post/', CreatePost.as_view(), name='add_post'),

]
