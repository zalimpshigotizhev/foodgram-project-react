from django.shortcuts import get_object_or_404
from api.permissions import OwnerUserOrReadOnly
from djoser.views import UserViewSet as DjUserViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.serializers import (ShortRecipeSerializer,
                             TagSerializer,
                             IngredientSerializer,
                             RecipeSerializer,
                             UserSubscribeSerializer)
from recipes.models import (Favorite,
                            Tag,
                            Ingredient,
                            CountIngredient,
                            Recipe,
                            Cart)
from users.models import CustomUser, Subscribe
from api.paginators import CustomPagination
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.status import (HTTP_400_BAD_REQUEST,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_201_CREATED)
from api import permissions
from django.http import HttpResponse
from django.db.models import Q


User = get_user_model()


class CustomUserViewSet(DjUserViewSet):
    pagination_class = CustomPagination
    add_serializer = UserSubscribeSerializer
    link_model = Subscribe

    @action(detail=True, permission_classes=(OwnerUserOrReadOnly,))
    def subscribe(self, request, id):
        '''

            Этот метод просто добавляет эндпоинт в виде
                    "api/users/{id}/subscribe/",
            помимо этого он является декоратором либо для
         create_subscribe[POST], либо для delete_subscribe[DELETE]

        '''

    @subscribe.mapping.post
    def create_subscribe(self, request, id):
        author = get_object_or_404(CustomUser, id=id)

        existing_subscription = Subscribe.objects.filter(user=request.user,
                                                         author=author).first()
        if existing_subscription:
            return Response({'error':
                             'Вы уже подписаны на этого автора'},
                            status=HTTP_400_BAD_REQUEST)
        if request.user.username == author.username:
            return Response({'error':
                             'Вы не можете подписаться на самого себя'},
                            status=HTTP_400_BAD_REQUEST)
        # Создайте новую подписку
        subscription = Subscribe.objects.create(user=request.user,
                                                author=author)
        subscription.save()
        serializer = self.add_serializer(author)

        return Response(serializer.data,
                        status=HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        author = get_object_or_404(CustomUser, id=id)

        try:
            subscription = Subscribe.objects.get(user=request.user,
                                                 author=author)
        except Subscribe.DoesNotExist:
            return Response({'error': 'Вы уже отписались!'},
                            status=HTTP_400_BAD_REQUEST)

        subscription.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=("get",), detail=False)
    def subscriptions(self, request):
        pages = self.paginate_queryset(
            User.objects.filter(subscribers__user=self.request.user)
        )
        serializer = UserSubscribeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (permissions.AdminOrReadOnly,)

    def get_queryset(self):
        query = self.request.query_params.get('name', '').strip().lower()
        queryset = Ingredient.objects.filter(Q(name__startswith=query) |
                                             Q(name__icontains=query))
        return queryset


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.AuthorStaffOrReadOnly,)
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    add_serializer = ShortRecipeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        query_params = self.request.query_params
        is_favorited = query_params.get('is_favorited')
        carts = query_params.get('is_in_shopping_cart')
        tags = query_params.getlist('tags')

        if carts == '1':
            queryset = queryset.filter(in_carts__user=user)

        if is_favorited == '1':
            queryset = queryset.filter(is_favorited__user=user)

        if tags:
            queryset = queryset.filter(tags__slug__in=tags)
        return queryset

    @action(detail=True)
    def favorite(self, request, pk):
        '''
        Аналогичная функция, что и с User.
        Данная функцию является маршрутом
        либо для POST, либо для DELETE.

        '''

    @favorite.mapping.post
    def create_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        existing_favorite = Favorite.objects.filter(user=request.user,
                                                    recipe=recipe).first()
        if existing_favorite:
            return Response({'errors':
                            'Вы уже добавили этот рецепт в избранное'},
                            status=HTTP_400_BAD_REQUEST)
        favorite = Favorite.objects.create(user=request.user,
                                           recipe=recipe)
        serializer = self.add_serializer(recipe)
        favorite.save()
        return Response(serializer.data,
                        status=HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        try:
            is_favorite = Favorite.objects.filter(user=request.user,
                                                  recipe=recipe)
        except Favorite.DoesNotExist:
            return Response({'errors':
                             'Рецепт и так не является фаворитом!'},
                            status=HTTP_400_BAD_REQUEST)
        is_favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=True)
    def shopping_cart(self, request, pk):
        '''
        Аналогичная функция, что и с User.
        Данная функцию является маршрутом
        либо для POST, либо для DELETE.

        '''

    @shopping_cart.mapping.post
    def create_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        existing_cart = Cart.objects.filter(user=request.user,
                                            recipe=recipe).first()
        if existing_cart:
            return Response({'errors':
                             'Вы уже добавили этот рецепт в список покупок'},
                            status=HTTP_400_BAD_REQUEST)

        link_cart = Cart.objects.create(user=request.user,
                                        recipe=recipe)
        link_cart.save()
        serializer = self.add_serializer(recipe)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        try:
            is_cart = Cart.objects.get(user=request.user,
                                       recipe=recipe)
        except Cart.DoesNotExist:
            return Response({'errors':
                             'Рецепт и так не добавлен в список покупок!'},
                            status=HTTP_400_BAD_REQUEST)
        is_cart.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=("get",))
    def download_shopping_cart(self, request):
        user = self.request.user
        recipes = Recipe.objects.filter(in_carts__user=request.user)
        ingredients_list = {}
        for recipe in recipes:
            ingredients = recipe.ingredients.all()

            for ingredient in ingredients:
                amount = CountIngredient.objects.get(
                    recipe=recipe,
                    ingredient=ingredient).amount

                if ingredients_list.get(str(ingredient), False):
                    ingredients_list[str(ingredient)] += amount
                else:
                    ingredients_list[str(ingredient)] = amount
        response = HttpResponse("\n".join(map(
            lambda ing: f"{str(ing[0])} - {ing[1]} ", ingredients_list.items()
        )),
                                content_type="text/plain",)
        response["Content-Disposition"] = (
            f'attachment; filename="{str(user)}_shopping_cart.txt"'
            )
        return response
