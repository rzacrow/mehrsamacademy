from rest_framework import generics
from blog.models import BlogPost, SavedPosts, BlogComments, BlogCategory
from blog.serializers import (
    PostSerializer,
    BlogPostSerializer,
    CategorySerializer,
    SavedPostsSerializer,
    CommonPostSerializer,
    BlogCommentsSerializer,
    CreateDeleteSavedPostsSerializer,
    CreateCommentsSerializer,
)
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class PostView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        instance = self.get_object()    
        response = CommonPostSerializer(instance)
        return Response(response.data)


class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by("published_at")
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category"]
    search_fields = ["title"]
    search_param = 'title'


class SavedPostsLitView(generics.ListAPIView):
    serializer_class = SavedPostsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SavedPosts.objects.filter(user=user)


class CreateSavedPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = Token.objects.get(key=request.auth.key).user
        data = {"user": user.id, "post": request.data["post"]}
        serializer = CreateDeleteSavedPostsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DeleteSavedPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            saved_post = SavedPosts.objects.get(
                user=request.user, post=request.data.get("post")
            )
            saved_post.delete()
            return Response(status=204)
        except SavedPosts.DoesNotExist:
            return Response(status=404)


class CommentsList(generics.ListAPIView):
    serializer_class = BlogCommentsSerializer

    def get_queryset(self):
        post = BlogPost.objects.get(slug=self.request.data["slug"])
        return BlogComments.objects.filter(post=post)

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = BlogCategory.objects.all()


class CreateComment(generics.CreateAPIView):
    serializer_class = CreateCommentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        response_serializer = BlogCommentsSerializer(instance)
        self.response_data = response_serializer.data

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request.data['post'] = BlogPost.objects.get(slug = request.data['post']).id
        response = super().create(request, *args, **kwargs)
        response.data = self.response_data
        return response
    
class PromotedListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_promoted=True).order_by("published_at")
    serializer_class = BlogPostSerializer
    print("Test")