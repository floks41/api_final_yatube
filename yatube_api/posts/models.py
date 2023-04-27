"""модуль моделей приложения Posts."""


from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Сообщества."""
    title = models.CharField(
        max_length=200,
        verbose_name='наименование группы',
        help_text='Введите наименование новой группы',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='слаг группы',
        help_text='Введите слаг новой группы',
    )
    description = models.TextField(
        verbose_name='описание группы',
        help_text='Введите описание новой группы',
    )

    class Meta:
        """Настройки модели Group."""
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self) -> str:
        """Отображениние информации об объекте класса Group."""
        return self.title


class Post(models.Model):
    """Пост."""
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='группа',
        help_text='Группа, к которой будет относиться пост'
    )

    def __str__(self):
        """Отображениние информации об объекте класса Post."""
        return self.text


class Comment(models.Model):
    """Комментарий."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    """Подписка на авторов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик',
        help_text='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор',
        help_text='Автор'
    )

    class Meta:
        """Настройки модели follow."""
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_author',
            ),

            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='users_cannot_follow_themselves',
            )
        ]
