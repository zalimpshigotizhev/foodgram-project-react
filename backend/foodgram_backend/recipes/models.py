from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    ''' Тэги '''
    name = models.CharField(
        ('название тэга'),
        max_length=64,
        unique=True,
    )
    color = models.CharField(
        ('цвет'),
        max_length=64,

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

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        ('наименование'),
        max_length=64,
        unique=True,

    )
    measurement_unit = models.CharField(
        ('единица измерения'),
        max_length=64,

    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    ''' Рецепты '''
    author = models.ForeignKey(
        User,
        verbose_name=("Автор"),
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        blank=False,

    )

    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=False,
    )
    image = models.ImageField(
        ('картинка'),
        upload_to='recipe_img/',
        blank=True,
    )
    name = models.CharField(
        ('название рецепта'),
        max_length=56
    )
    text = models.TextField(
        ('текст'),
        max_length=1024
    )
    cooking_time = models.PositiveIntegerField(
        ('время приготовления'),
        default=0,
        validators=(
            MinValueValidator(
                1,
                'Нужно указать время приготовления'
            ),
            MaxValueValidator(
                500,
                'Слишком долго готовить!'
            )
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

