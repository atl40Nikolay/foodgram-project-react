from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token

MAX_EMAIL_LENGTH = 254
MAX_NAMES_LENGTH = 150


class MyToken(Token):
    class Meta:
        proxy = True
        verbose_name = 'токен'
        verbose_name_plural = 'токены'


class User(AbstractUser):
    """Кастомный класс для User."""
    email = models.EmailField(
        'электронная почта',
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        blank=False,
        help_text='Адрес электронной почты.',
    )
    first_name = models.CharField(
        'имя',
        max_length=MAX_NAMES_LENGTH,
        help_text='Имя.'
    )
    last_name = models.CharField(
        'фамилия',
        max_length=MAX_NAMES_LENGTH,
        help_text='Фамилия.'
    )
    follows = models.ManyToManyField(
        to='self',
        verbose_name='Подписка',
        related_name='followers',
        through='Follow',
        symmetrical=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return bool(self.is_superuser or self.is_staff)

    class Meta:
        ordering = ("id",)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик',
        help_text='Подписчик.',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed',
        verbose_name='автор',
        help_text='Автор рецептов.',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_follow'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}.'
