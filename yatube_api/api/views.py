"""Модуль представлений приложения Api, для моделей приложения Posts."""


from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from django.shortcuts import get_object_or_404
from posts.models import Group, Post
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class ApiBaseModelViewSet(viewsets.ModelViewSet):
    """Базовый класс для viewset`ов приложения."""
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)


class PostViewSet(ApiBaseModelViewSet):
    """Представление для модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создание записи.
        При создании записи автором автоматически
        устанавливается аутентифицированный пользователь.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'slug', 'description')


class CommentViewSet(ApiBaseModelViewSet):
    """Представление для модели Comment."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Устанавливает набор записей модели Comment.
        Фильтруются записи, относящиеся к посту,
        идентификатор которого указан в пути к эндпоинту.
        """
        return (
            get_object_or_404(Post, pk=self.kwargs['post_id']).comments.all()
        )

    def perform_create(self, serializer):
        """Создание записи.
        При создании записи автором автоматически
        устанавливается аутентифицированный пользователь.
        Пост, к которому относится комментарий, устанавливается
        по идентификатору указанному в пути к эндпоинту.
        """
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, pk=self.kwargs['post_id'])
        )


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    """Представление для модели Follow."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Устанавливает набор записей сериализатора модели Follow.
        Фильтруются записи, где текущий пользователь является подписчиком.
        """
        return self.request.user.follower.all()

    def perform_create(self, serializer: serializers.Serializer):
        """Создание записи.
        При создании записи подписчиком автоматически
        устанавливается аутентифицированный пользователь.
        """
        return serializer.save(user=self.request.user)
