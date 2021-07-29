from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import *
from django import forms


# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = Post
#         fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'category', 'created_at', 'get_photo', 'views', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', 'tags', 'author')
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ('title', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at', 'author')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Фото'


class CategoryAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)


class TagAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'active')
    list_filter = ('active', 'created_at', 'updated_at')
    search_fields = ('author',  'body')


# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('nickname', )
#     list_display_links = ('nickname', )
#     search_fields = ('nickname', )
#     # prepopulated_fields = {'slug': ('nickname',)}


admin.site.register(Post, PostAdmin)
# admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
