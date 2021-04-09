from django.urls import path
from .views import ArticlesAPIView, ArticleDetailAPIView

urlpatterns = [
    path('', ArticlesAPIView.as_view(), name='articles'),
    path('my/', ArticleDetailAPIView.as_view(), name='article'),
]