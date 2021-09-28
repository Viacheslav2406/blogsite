from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import *
from .forms import UserLoginForm, UserRegisterForm, PostForm, CommentForm, RelationForm, TagForm, SendPostEmail
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.db.models import F, Q


def contact(request):
    if request.method == 'POST':
        form = RelationForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],'Viacheslavtest24@gmail.com', [form.cleaned_data['email']], fail_silently=False)

            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = RelationForm()
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


class UpdatePost(SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update_post.html'
    success_message = 'Пост успешно отредактирован'
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'slug': self.get_object().slug})


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


def get_popular_posts(request):
    posts = Post.objects.order_by('-views')[:5]
    return render(request, 'blog/popular_posts.html', {'posts': posts})


def send_post_to_email(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == "POST":
        form = SendPostEmail(request.POST)
        if form.is_valid():
            mail = send_mail(post.title, post.content, 'Viacheslavtest24@gmail.com', [form.cleaned_data['email']], fail_silently=False)
            if mail:
                messages.success(request, 'Пост успешно отправлен')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка отправки')

        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = SendPostEmail()
    return render(request, 'blog/send_post.html', {'form': form})


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

class DeleteComment(DeleteView):
    model = Comment
    template_name = 'blog/single_post.html'

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Комментарий успешно удален')
        return self.delete(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        post = Post.objects.get(comments=self.get_object())
        return reverse_lazy('post', kwargs={'slug': post.slug})


class CreateTag(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'blog/add_tag.html'
    success_url = reverse_lazy('add_tag')


class MyPosts(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5
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
    paginate_by = 5
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
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(Q(title__icontains=self.request.GET.get('s'))|
                                   Q(content__icontains=self.request.GET.get('s'))|
                                   Q(tags__title__icontains=self.request.GET.get('s')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context

