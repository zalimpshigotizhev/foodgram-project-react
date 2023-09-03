from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    '''  Кастомный юзер  '''
    email = models.EmailField(
        verbose_name="Электронная почта",
        unique=True,
    )

    first_name = models.CharField(
        verbose_name="Имя",
        max_length=64,

    )

    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=64,

    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=128,
    )
    is_active = models.BooleanField(
        verbose_name="Активирован",
        default=True
    )

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subscription(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='subscribers')
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.author.username}"
