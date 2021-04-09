import os
from article.google import Google
from rest_framework import serializers
from .models import Article, ImageTest
from rest_framework.exceptions import AuthenticationFailed

class ArticleSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    is_approved = serializers.BooleanField(read_only=True)
    class Meta:
        model = Article
        fields = ['title', 'content', 'created_by', 'date_created', 'is_approved']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTest
        fields = '__all__'


