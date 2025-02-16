from django.contrib import admin
from .models import Comment, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админка для модели Post"""
    list_display = ('pk', 'pub_date', 'author')
    search_fields = ('text', 'author__username')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Админка для модели Group"""
    list_display = ('pk', 'title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для модели Comment"""
    list_display = ('pk', 'author', 'post', 'created')
    search_fields = ('text', 'author__username')
    list_filter = ('created',)
    empty_value_display = '-пусто-'
