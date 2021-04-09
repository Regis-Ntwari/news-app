from rest_framework import permissions
from article.permissions import IsOwner
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.permissions import AllowAny

# Create your views here.
from .models import Article, ImageTest
from .serializers import ArticleSerializer, ImageSerializer

class ArticlesAPIView(generics.ListAPIView):
    permission_classes = []
    queryset = Article.objects.all().filter(is_approved=True)
    serializer_class = ArticleSerializer

class ArticleDetailAPIView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)


class ImageTesting(viewsets.ModelViewSet):
    permission_classes = []
    queryset = ImageTest.objects.all()
    serializer_class = ImageSerializer

# class UserCreate(generics.CreateAPIView):
#     permission_classes = [AllowAny, ]
#     serializer_class = UserSerializer

# class UserList(generics.ListAPIView):
#     permission_classes = [AllowAny, ]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class ImageHandler(APIView):
#     def post(self, request):
#         parser_classes = [MultiPartParser, FormParser]
#         serializer = ImageSerializer(data=request.data)
#         if(serializer.is_valid()):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request):
#         images = ImageTest.objects.all()
#         data = ImageSerializer(images, many=True).data
#         return Response(data)


# class UserCreate(generics.CreateAPIView):
#     authentication_classes = ()
#     permission_classes = ()
#     serializer_class = UserSerializer

# class LoginView(APIView):
#     permission_classes = ()
    
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)

#         if user:
#             return Response({"token" : user.auth_token.key})
#         else:
#             return Response({"error" : "Wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)