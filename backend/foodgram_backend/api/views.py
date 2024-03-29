from collections import defaultdict

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.status import (HTTP_400_BAD_REQUEST,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_201_CREATED)
from djoser.views import UserViewSet as DjUserViewSet

from users.models import CustomUser, Subscribe
from api.paginators import CustomPagination, RecipePagination
from api.permissions import OwnerUserOrReadOnly
from recipes.models import (Tag,
                            Ingredient,
                            CountIngredient,
                            Recipe,)
from api.serializers import (FavoriteSerializer, ShortRecipeSerializer,
                             TagSerializer,
                             IngredientSerializer,
                             RecipeSerializer,
                             SubscribeSerializer,
                             UserSubscribeSerializer)
from api.permissions import (AdminOrReadOnly,
                             AuthorStaffOrReadOnly)

User = get_user_model()


class CustomUserViewSet(DjUserViewSet):
    pagination_class = CustomPagination
    add_serializer = UserSubscribeSerializer
    link_model = Subscribe

    @action(detail=True, permission_classes=(OwnerUserOrReadOnly,))
    def subscribe(self, request, id):
        """

            Этот метод просто добавляет эндпоинт в виде
                    "api/users/{id}/subscribe/",
            помимо этого он является декоратором либо для
         create_subscribe[POST], либо для delete_subscribe[DELETE]

        """

    @subscribe.mapping.post
    def create_subscribe(self, request, id):
        author = get_object_or_404(CustomUser, id=id)

        subscribe_serializer = SubscribeSerializer(data=request.data,
                                                   context={"request": request,
                                                            "author": author})
        subscribe_serializer.is_valid(raise_exception=True)
        subscribe_serializer.save(user=request.user, author=author)
        return Response(subscribe_serializer.data, status=HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        author = get_object_or_404(CustomUser, id=id)

        subscription = author.subscribers.filter(user=request.user).first()
        if subscription is None:
            return Response({"error": "Вы уже отписались!"},
                            status=HTTP_400_BAD_REQUEST)
        subscription.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=("get",), detail=False, pagination_class=RecipePagination)
    def subscriptions(self, request):
        pages = self.paginate_queryset(
            User.objects.filter(subscribers__user=self.request.user)
        )
        serializer = UserSubscribeSerializer(pages, many=True,
                                             context={"request": request})
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AdminOrReadOnly,)

    def get_queryset(self):
        query = self.request.query_params.get("name", " ").strip().lower()
        return Ingredient.objects.filter(
            Q(name__startswith=query) | Q(name__icontains=query)
        )


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorStaffOrReadOnly,)
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    add_serializer = ShortRecipeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        query_params = self.request.query_params
        is_favorited = query_params.get("is_favorited")
        carts = query_params.get("is_in_shopping_cart")
        tags = query_params.getlist("tags")
        author = query_params.get("author")

        if author:
            queryset = queryset.filter(author=author)

        if carts == "1":
            queryset = queryset.filter(in_carts__user=user)

        if is_favorited == "1":
            queryset = queryset.filter(is_favorited__user=user)

        if tags:
            return queryset.filter(tags__slug__in=tags).distinct()
        return queryset

    @action(detail=True)
    def favorite(self, request, pk):
        """
            Аналогичная функция, что и с User.
            Данная функцию является маршрутом
            либо для POST, либо для DELETE.

        """

    @favorite.mapping.post
    def create_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        favorite_serializer = FavoriteSerializer(
            data=request.data,
            context={"request": request,
                     "recipe": recipe})
        favorite_serializer.is_valid(raise_exception=True)
        favorite_serializer.save(user=request.user,
                                 recipe=recipe)
        return Response(favorite_serializer.data,
                        status=HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        is_favorite = recipe.is_favorited.filter(user=request.user).first()
        if is_favorite is None:
            return Response({"errors":
                            "Рецепт и так не является фаворитом!"},
                            status=HTTP_400_BAD_REQUEST)
        is_favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=True)
    def shopping_cart(self, request, pk):
        """
            Аналогичная функция, что и с User.
            Данная функцию является маршрутом
            либо для POST, либо для DELETE.

        """

    @shopping_cart.mapping.post
    def create_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        existing_cart = request.user.in_carts.filter(recipe=recipe).first()
        if existing_cart:
            return Response({"errors":
                             "Вы уже добавили этот рецепт в список покупок"},
                            status=HTTP_400_BAD_REQUEST)

        link_cart = recipe.in_carts.create(user=request.user)
        link_cart.save()
        serializer = self.add_serializer(recipe)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        cart = recipe.in_carts.filter(user=request.user).first()
        if cart is None:
            return Response({"errors":
                             "Рецепт и так не добавлен в список покупок!"},
                            status=HTTP_400_BAD_REQUEST)
        cart.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=("get",))
    def download_shopping_cart(self, request):
        user = self.request.user
        recipes = Recipe.objects.filter(in_carts__user=request.user)

        ingredients_list = defaultdict(int)

        for recipe in recipes:
            ingredients = recipe.ingredients.all()

            for ingredient in ingredients:
                amount = CountIngredient.objects.get(
                    recipe=recipe,
                    ingredient=ingredient).amount

                ingredients_list[str(ingredient)] += amount

        response = HttpResponse(
            "\n".join(
                [f"{ingredient} - {amount}"
                 for ingredient, amount in ingredients_list.items()]
            ), content_type="text/plain"
        )

        response["Content-Disposition"] = (
            f"attachment; filename={str(user)}_shopping_cart.txt")

        return response
