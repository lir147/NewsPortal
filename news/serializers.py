from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(source='author.user', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'categories', 'comments',
                  'created_at', 'post_type', 'rating', 'is_published']


# Добавляем недостающие сериализаторы
class NewsSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        pass


class ArticleSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        pass


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'post_type', 'is_published']