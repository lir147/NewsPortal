import django_filters
from django import forms
from .models import Post

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    author__username = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains', label='Имя автора')
    created_at = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Дата позже',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author__username', 'created_at']