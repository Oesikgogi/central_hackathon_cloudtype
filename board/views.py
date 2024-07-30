# community/board/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics
from .models import Facility
from .serializers import FacilitySerializer
from .filters import FacilityFilter
from django_filters.rest_framework import DjangoFilterBackend

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = serializer.data
        response_data["comments"] = []
        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = [
            {
                "id": post["id"],
                "user": post["user"],
                "nickname": post["nickname"],
                "title": post["title"],
                "created_at": post["created_at"]
            }
            for post in serializer.data
        ]
        return Response(response_data)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        response_data["comments"] = [
            {
                "id": comment.id,
                "user": comment.user.id,
                "nickname": comment.user.profile.nickname,
                "comment": comment.comment,
                "created_at": comment.created_at.strftime("%Y-%m-%d")
            }
            for comment in instance.comments.all()
        ]
        return Response(response_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        post = self.get_object()
        response_data = {
            "id": post.id,
            "user": post.user.id,
            "nickname": post.user.profile.nickname,
            "title": post.title,
            "body": post.body,
            "created_at": post.created_at.strftime("%Y-%m-%d"),
            "comments": [
                {
                    "id": comment.id,
                    "user": comment.user.id,
                    "nickname": comment.user.profile.nickname,
                    "comment": comment.comment,
                    "created_at": comment.created_at.strftime("%Y-%m-%d"),
                }
                for comment in post.comments.all()
            ]
        }
        return Response(response_data, status=status.HTTP_200_OK)

class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs['post_id'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        post = Post.objects.get(pk=self.kwargs['post_id'])
        response_data = {
            "id": post.id,
            "user": post.user.id,
            "nickname": post.user.profile.nickname,
            "title": post.title,
            "body": post.body,
            "created_at": post.created_at.strftime("%Y-%m-%d"),
            "comments": [
                {
                    "id": comment.id,
                    "user": comment.user.id,
                    "nickname": comment.user.profile.nickname,
                    "comment": comment.comment,
                    "created_at": comment.created_at.strftime("%Y-%m-%d"),
                }
                for comment in post.comments.all()
            ]
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(post_id=self.kwargs['post_id'])

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        post = Post.objects.get(pk=self.kwargs['post_id'])
        response_data = {
            "id": post.id,
            "user": post.user.id,
            "nickname": post.user.profile.nickname,
            "title": post.title,
            "body": post.body,
            "created_at": post.created_at.strftime("%Y-%m-%d"),
            "comments": [
                {
                    "id": comment.id,
                    "user": comment.user.id,
                    "nickname": comment.user.profile.nickname,
                    "comment": comment.comment,
                    "created_at": comment.created_at.strftime("%Y-%m-%d"),
                }
                for comment in post.comments.all()
            ]
        }
        return Response(response_data, status=status.HTTP_200_OK)

class FacilityListView(generics.ListAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FacilityFilter
