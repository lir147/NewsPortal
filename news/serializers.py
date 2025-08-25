from rest_framework import serializers
from .models import News, Article, Category, Comment, AuthorProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class AuthorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AuthorProfile
        fields = ['id', 'user', 'bio', 'profile_picture', 'is_author']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'rating']
        read_only_fields = ['created_at']


class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'author', 'category', 'category_id',
            'created_at', 'updated_at', 'is_published', 'comments',
            'likes_count', 'dislikes_count', 'rating'
        ]
        read_only_fields = ['created_at', 'updated_at', 'author', 'likes_count', 'dislikes_count', 'rating']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'author', 'category', 'category_id',
            'created_at', 'updated_at', 'is_published', 'comments',
            'likes_count', 'dislikes_count', 'rating'
        ]
        read_only_fields = ['created_at', 'updated_at', 'author', 'likes_count', 'dislikes_count', 'rating']


# Сериализаторы для создания/обновления
class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'is_published']


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'is_published']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']