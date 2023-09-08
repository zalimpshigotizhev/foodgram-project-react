from django.contrib import admin
from .models import (
    Recipe,
    Tag,
    Ingredient,
    Favorite,
    AmountIngredient,
    Cart
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ...


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    ...


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    ...


@admin.register(AmountIngredient)
class AmountIngredientAdmin(admin.ModelAdmin):
    ...
