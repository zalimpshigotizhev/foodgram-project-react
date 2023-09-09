from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        EmailField,
                                        CharField,
                                        ReadOnlyField)
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Tag, Ingredient, CountIngredient
from users.models import Subscribe
from drf_extra_fields.fields import Base64ImageField
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_201_CREATED)

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
        read_only_fields = ("__all__",)
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
        fields = '__all__'
        read_only_fields = ("__all__",)


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ("__all__",)


class IngredientAmountSerializer(ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()

    class Meta:
        model = CountIngredient
        fields = ('id', 'amount', 'name', 'measurement_unit')
        read_only_fields = ("__all__",)

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
        serialized_ingredients = IngredientAmountSerializer(ingredients,
                                                      many=True).data
        return serialized_ingredients
    
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
    
    # def create(self, validated_data:dict):
    #     # data_ingredients = validated_data['ingredients']
    #     # data_tags = validated_data['tags']
    #     # for data_ingredient in data_ingredients:
            
    #     #     measurement_unit = ingredient['measurement_unit']
    #     #     new_ingredient = Ingredient.objects.create(name=name,
    #     #                                                measurement_unit=measurement_unit)
    #     #     new_ingredient.save()
    #     user = self.context['request'].user
    #     # ingredients = validated_data['ingredients']
    #     # tags = validated_data['tags']
    #     recipe = Recipe.objects.create(author=user, **validated_data)
    #     # recipe.tags.set(tags)
    #     return recipe
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


class ShortRecipeSerializer(ModelSerializer):
    """Сериализатор для модели Recipe.
    Определён укороченный набор полей для некоторых эндпоинтов.
    """

    class Meta:
        model = Recipe
        fields = "id", "name", "image", "cooking_time"
        read_only_fields = ("__all__",)


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
        read_only_fields = ("__all__",)

    def get_is_subscribed(*args):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()
