from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin

from .models import *
from .forms import UserLoginForm, UserRegisterForm, PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.db.models import F


def contact(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['title'], form.cleaned_data['content'],'v.bakalo24@ukr.net', ['v.bakalo24@gmail.com'], fail_silently=False)
            form.save()
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = PostForm()
    return render(request, 'blog/contact.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


class UpdatePost(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update_post.html'
    success_url = reverse_lazy('update_post')
    raise_exception = True


class DeletePost(DeleteView):
    model = Post
    template_name = 'blog/single_post.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Пост успешно удален')
        return self.delete(request, *args, **kwargs)


class CreatePost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('home')
    raise_exception = True

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePost, self).form_valid(form)


class ViewPost(DetailView, FormMixin):
    model = Post
    template_name = 'blog/single_post.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Комментарий создан')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class PostsByAuthor(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


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


def search(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(title__icontains=search_query)
    else:
        posts = Post.objects.all()

    return render(request, 'blog/search.html', context=posts)


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"{self.request.GET.get('s')}&"
        return context

