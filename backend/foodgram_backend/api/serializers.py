from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from django.core.exceptions import ValidationError
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        EmailField,
                                        CharField,)

from api.core import id_and_amount_pull_out_from_dict
from recipes.models import Recipe, Tag, Ingredient, CountIngredient


User = get_user_model()


class CustomUserSerializer(ModelSerializer):
    email = EmailField(required=True)
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_subscribed"
        )
        read_only_fields = "is_subscribed",
        extra_kwargs = {"password": {"write_only": True}}

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscriptions.filter(author=obj).exists()

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = "__all__",


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"
        read_only_fields = "__all__",


class IngredientAmountSerializer(ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()

    class Meta:
        model = CountIngredient
        fields = ('id', 'amount', 'name', 'measurement_unit')
        # read_only_fields = "__all__"

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_id(self, obj):
        return obj.ingredient.id


class RecipeSerializer(ModelSerializer):
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')
        read_only_fields = (
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_ingredients(self, obj):
        ingredients = CountIngredient.objects.filter(recipe=obj)
        return IngredientAmountSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.is_favorited.filter(user=user).exists()
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get("view").request.user
        if user.is_anonymous:
            return False
        return user.in_carts.filter(recipe=recipe).exists()

    def validate(self, data):
        data_ingredients = self.initial_data.get('ingredients')
        id_tags = self.initial_data.get('tags')

        if not data_ingredients or not id_tags:
            raise ValidationError('Заполните все поля и картинку не забудьте!')

        list_id_amount = id_and_amount_pull_out_from_dict(Ingredient,
                                                          data_ingredients)

        # Нахождение тэгов

        try:
            tags_obj = Tag.objects.filter(id__in=id_tags)
        except Tag.DoesNotExist:
            raise ValueError("Такого тэга нет")

        data.update(
            {
                'ingredients': list_id_amount,
                'tags': tags_obj,
            }
        )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        new_recipe = Recipe.objects.create(author=user, **validated_data)
        amount_ingr = [
            CountIngredient(ingredient=value[0],
                            amount=value[1],
                            recipe=new_recipe) for value in ingredients
        ]
        CountIngredient.objects.bulk_create(amount_ingr)
        new_recipe.tags.set(tags)
        return new_recipe

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)

        instance.save()

        ingredients_data = validated_data.get('ingredients')
        if ingredients_data is not None:
            instance.ingredients.clear()
            amount_ingr = [
                CountIngredient(ingredient=value[0],
                                amount=value[1],
                                recipe=instance) for value in ingredients_data
            ]
        CountIngredient.objects.bulk_create(amount_ingr)

        tags_data = validated_data.get('tags')
        if tags_data is not None:
            instance.tags.set(tags_data)

        return instance


class ShortRecipeSerializer(ModelSerializer):
    """
    Сериализатор для модели Recipe.
    Короткий вид рецептов для подписок на юзера.

    """

    class Meta:
        model = Recipe
        fields = "id", "name", "image", "cooking_time"
        read_only_fields = "__all__",


class UserSubscribeSerializer(CustomUserSerializer):
    """Сериализатор вывода авторов на которых подписан текущий пользователь."""

    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = "__all__"

    def get_is_subscribed(*args):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()
