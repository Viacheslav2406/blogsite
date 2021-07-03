from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy


class UpdatePost(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update_post.html'
    success_url = reverse_lazy('home')
    raise_exception = True


class DeletePost(DeleteView):
    pass


class CreatePost(CreateView):
    form_class = PostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('home')
    raise_exception = True


class ViewPost(DetailView):
    model = Post
    template_name = 'blog/single_post.html'
    context_object_name = 'post'


class PostsByAuthor(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(author__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Author.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context

