from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        prepopulated_fields = {'slug': ('title',)}
        fields = ['title', 'content', 'category', 'tags', 'author',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }