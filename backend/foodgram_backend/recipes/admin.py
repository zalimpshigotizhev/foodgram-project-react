from django.contrib import admin
from .models import (
    Recipe,
    Tag,
    Ingredient,
    Favorite
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
