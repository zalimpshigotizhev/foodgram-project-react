from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from PIL import Image

from api.core import (DEFAULT_INGR,
                      MAX_SIZE_IMAGE,
                      MAX_TIME_COOK,
                      MIN_TIME_COOK)

User = get_user_model()


class Tag(models.Model):
    """ Тэги """

    name = models.CharField(
        ('название тэга'),
        max_length=64,
        unique=True,
    )
    color = models.CharField(
        ('цвет'),
        max_length=64,
        unique=True,

    )
    slug = models.CharField(
        ('слаг'),
        max_length=64,
        unique=True,
        db_index=False
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def clean(self) -> None:
        if len(self.color) != 6:
            raise ValidationError("Для цвета нужно 6 символов")
        self.color = '#' + self.color.upper()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Ингредиент """

    name = models.CharField(
        ('наименование'),
        max_length=64,
        unique=True,)

    measurement_unit = models.CharField(
        ('единица измерения'),
        max_length=64,)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Рецепты """

    name = models.CharField(
        verbose_name=('Название рецепта'),
        max_length=56)

    author = models.ForeignKey(
        User,
        verbose_name=('Автор'),
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True)

    tags = models.ManyToManyField(
        Tag,
        verbose_name=('Тэги'),
        related_name='recipes',
        blank=False,)

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name=('Ингредиенты'),
        blank=False,
        related_name='recipes',
        through='CountIngredient',)

    pub_date = models.DateTimeField(
        verbose_name=('Дата и время публикации'),
        auto_now_add=True,
        editable=False)

    image = models.ImageField(
        verbose_name=('Картинка'),
        upload_to='recipe_img/',)

    text = models.TextField(
        verbose_name=('Текст'),
        max_length=1024)

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=('Время приготовления'),
        default=DEFAULT_INGR,
        validators=(
            MinValueValidator(
                MIN_TIME_COOK,
                'Нужно указать время приготовления'
            ),
            MaxValueValidator(
                MAX_TIME_COOK,
                'Слишком долго готовить!'
            )
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)
        image.thumbnail(MAX_SIZE_IMAGE)
        image.save(self.image.path)


class CountIngredient(models.Model):
    """ Количество ингридиентов в блюде """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE)

    amount = models.PositiveSmallIntegerField(
        verbose_name=('Количество'),
        default=1,
        validators=(
            MinValueValidator(
                1,
                'Нужен хоть грамм/мл!'
            ),
            MaxValueValidator(
                3200,
                'Слишком много!')
        )
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ("recipe",)

    def __str__(self) -> str:
        return f"{self.amount} {self.ingredient}"


class Favorite(models.Model):
    """ Избранные рецепты """

    user = models.ForeignKey(
        User,
        related_name='in_favorites',
        verbose_name=('пользователь'),
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='is_favorited',
        verbose_name=('рецепт'),
        on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(
        verbose_name='Дата и время add',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self) -> str:
        return f'{self.user} добавил в фавориты рецепт {self.recipe}'


class Cart(models.Model):
    """ Список покупок """

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты списка покупок',
        related_name='in_carts',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Автор списка покупок',
        related_name='in_carts',
        on_delete=models.CASCADE
    )
    date_add = models.DateTimeField(
        verbose_name='Дата и время добавления',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ["recipe"]

    def __str__(self):
        return f'{self.user} добавил в список покупок {self.recipe}'
