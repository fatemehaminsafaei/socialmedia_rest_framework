from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView, get_object_or_404
)
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status as s
from django.shortcuts import get_list_or_404

from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer
from ..permissions import IsAuthorOrReadOnly


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    lookup_field = 'uuid'
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        return serializer.save(edited= True)


class PinPostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, uuid):
        """
        Increment post pins by 1.
        """
        post = get_object_or_404(Post, uuid=uuid)
        post.pins += 1
        post.save()
        return Response(status=s.HTTP_200_OK)


class CommentListCreateAPIView(ListCreateAPIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.order_by('-date_created').filter(
           post__uuid = self.kwargs['uuid']
        )

    def perform_create(self, serializer):
        post = Post.objects.get(uuid=self.kwargs['uuid'])
        return serializer.save(author= self.request.user, post= post)


class CommentRetrieveDestroyAPIView(RetrieveDestroyAPIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self):
        comment = get_object_or_404(Comment, uuid=self.kwargs['comment_uuid'],
                                    post__uuid=self.kwargs['post_uuid'])
        self.check_object_permissions(self.request, comment)
        return comment

class UserPostListAPIView(ListAPIView):

    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.order_by('-date_created').filter(
            author__uuid = self.kwargs['uuid']
        )


class RecentPostsAPIView(ListAPIView):

    serializer_class = PostSerializer
    queryset = Post.objects.order_by('-date_created').all()









