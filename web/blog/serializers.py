from blog.models import BlogCategory, BlogPost, BlogComments, SavedPosts
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.reverse import reverse
from accounts.serializers import UserCommentSerializer
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ('id', 'title', 'image')

class BlogPostSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'slug', "banner", 'caption',
                  'category', 'published_at','is_promoted', 'tag', 'absolute_url')
    def get_absolute_url(self, obj):
        return reverse('BlogPost',args=(obj.slug,))


class BlogCommentsSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer()
    class Meta:
        model = BlogComments
        fields = ('id', 'user', 'caption', 'written_at', 'post')


class PostSerializer(serializers.ModelSerializer):
    comments = BlogCommentsSerializer(many=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'slug', 'caption', 'content','category', 'published_at',
                  "banner", 'is_promoted', 'tag', 'comments')

class CommonPostSerializer(serializers.ModelSerializer):
    comments = BlogCommentsSerializer(many=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'slug', "banner", 'caption',
                  'category', 'published_at','is_promoted', 'tag', 'comments')

class SavedPostsSerializer(serializers.ModelSerializer):
    post = BlogPostSerializer()

    class Meta:
        model = SavedPosts
        fields = ('post',)

class CreateDeleteSavedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPosts
        fields = ['user', 'post']
        
class CreateCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComments
        fields = ('user', 'caption', 'written_at', 'post')