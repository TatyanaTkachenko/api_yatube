from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied

from posts.models import Post, Group

from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class OwnerActionMixin:
    """Миксин для проверки прав владельца и управления действиями"""


    def check_owner_permission(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                "У вас нет прав на "
                "выполнение этого действия!"
            )

    def perform_update(self, serializer):
        self.check_owner_permission(serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        self.check_owner_permission(instance)
        instance.delete()


class PostViewSet(OwnerActionMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet, OwnerActionMixin):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_post(self):
        if not hasattr(self, '_post'):
            self._post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return self._post

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
