from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Группа для объединения постов по тематике
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Название группы",
        help_text="Введите название группы."
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="URL slug",
        help_text="Уникальное значение для формирования URL группы."
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Опишите группу."
    )

    class Meta:
        ordering = ['title']
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Пост, созданный пользователем
    """
    text = models.TextField(
        verbose_name="Текст поста",
        help_text="Введите содержание поста."
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Дата и время создания поста."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор",
        help_text="Пользователь, создавший пост."
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name="Изображение",
        help_text="Изображение к посту (необязательно)."
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name="Группа",
        help_text="Группа, к которой относится пост."
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        # Возвращаем первые 50 символов поста для краткого представления
        return self.text[:50]


class Comment(models.Model):
    """
    Комментарий к посту
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор комментария",
        help_text="Пользователь, оставивший комментарий."
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Пост",
        help_text="Пост, к которому оставлен комментарий."
    )
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="Введите текст комментария."
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления комментария."
    )

    class Meta:
        ordering = ['-created']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        # Возвращаем первые 50 символов комментария для краткого представления
        return self.text[:50]
