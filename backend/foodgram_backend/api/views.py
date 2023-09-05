from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjUserViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import (ShortRecipeSerializer, TagSerializer, IngredientSerializer,
                          RecipeSerializer, UserSubscribeSerializer,
                          UserSubscribeSerializer)
from recipes.models import Favorite, Tag, Ingredient, Recipe
from users.models import CustomUser, Subscribe
from .paginators import CustomPagination
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.status import (HTTP_400_BAD_REQUEST,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_201_CREATED)


User = get_user_model()


class CustomUserViewSet(DjUserViewSet):
    pagination_class = CustomPagination
    add_serializer = UserSubscribeSerializer
    link_model = Subscribe

    @action(detail=True)
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
            return Response({'detail': 'Вы уже подписаны на этого автора'},
                            status=HTTP_400_BAD_REQUEST)
        if request.user.username == author.username:
            return Response({'detail': 'Вы не можете подписаться на самого себя'},
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
            return Response({'errors':'Вы уже отписались!'},status=HTTP_400_BAD_REQUEST)

        subscription.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        methods=("get",), detail=False
    )
    def subscriptions(self, request):
        pages = self.paginate_queryset(
            User.objects.filter(subscribers__user=self.request.user)
        )
        serializer = UserSubscribeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


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
    add_serializer = ShortRecipeSerializer
    link_model = Subscribe

    @action(detail=True)
    def favorite(self, request, id):
        '''
        Аналогичная функция, что и с User.
        Данная функцию является маршрутом 
        либо для, POST либо для DELETE.

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
            is_favorite = Favorite.objects.get(user=request.user,
                                                 recipe=recipe)
        except Favorite.DoesNotExist:
            return Response({'errors':
                             'Рецепт и так не является фаворитом!'},
                            status=HTTP_400_BAD_REQUEST)
        is_favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)
