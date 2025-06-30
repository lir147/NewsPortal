from django.contrib import admin
from .models import Post, Author, Category, Comment

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')