from django import forms
from .models import Post,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш комментарий'})
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['post_type']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['post_type']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")