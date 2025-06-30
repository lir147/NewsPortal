from django import forms
from .models import Post

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['post_type']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['post_type']