from djoser.views import UserViewSet as DjUserViewSet
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, UserSubscribeSerializer
from recipes.models import Tag, Ingredient, Recipe
from users.models import Subscription
from .paginators import CustomPagination


class CustomUserViewSet(DjUserViewSet):
    pagination_class = CustomPagination
    add_serializer = UserSubscribeSerializer
    link_model = Subscription



class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
