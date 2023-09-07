from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from api.constants import Const
from PIL import Image

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
    name = models.CharField(
        verbose_name=("Название рецепта"),
        max_length=56
    )
    author = models.ForeignKey(
        User,
        verbose_name=("Автор"),
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=("Тэги"),
        related_name='recipes',
        blank=False,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name=("Ингредиенты"),
        related_name='recipes',
        blank=False,
    )
    pub_date = models.DateTimeField(
        verbose_name=("Дата и время публикации"),
        auto_now_add=True,
        editable=False
    )
    image = models.ImageField(
        verbose_name=("Картинка"),
        upload_to='recipe_img/',
    )
    text = models.TextField(
        verbose_name=("Текст"),
        max_length=1024
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name=("Время приготовления"),
        default=0,
        validators=(
            MinValueValidator(
                1,
                'Нужно указать время приготовления'
            ),
            MaxValueValidator(
                300,
                'Слишком долго готовить!'
            )
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)
        image.thumbnail(Const.RECIPE_IMAGE_SIZE)
        image.save(self.image.path)

class AmountIngredient(models.Model):
    """Количество ингридиентов в блюде. """

    recipe = models.ForeignKey(
        verbose_name="В каких рецептах",
        related_name="ingredient",
        to=Recipe,
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        verbose_name="Связанные ингредиенты",
        related_name="recipe",
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        default=0,
        validators=(
            MinValueValidator(
                1,
                "Нужно хоть какое-то количество.",
            ),
            MaxValueValidator(
                300,
                "Слишком много!",
            ),
        ),
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Количество ингридиентов"
        ordering = ("recipe",)

    def __str__(self) -> str:
        return f"{self.amount} {self.ingredients}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name="in_favorites",
        verbose_name="пользователь",
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="favorites",
        verbose_name="рецепт",
        on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(
        verbose_name="Дата и время add",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"

    def __str__(self) -> str:
        return f'{self.user} добавил в фавориты рецепт {self.recipe}'


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепты списка покупок",
        related_name='in_carts',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name="Автор списка покупок",
        related_name='in_carts',
        on_delete=models.CASCADE
    )
    date_add = models.DateTimeField(
        verbose_name="Дата и время добавления",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"

    def __str__(self):
        return f'{self.user} добавил в список покупок {self.recipe}'
