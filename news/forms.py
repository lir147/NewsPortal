from django import forms
from .models import Post,Comment

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