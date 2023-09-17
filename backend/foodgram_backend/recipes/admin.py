from django.contrib import admin

from .models import (
    Recipe,
    Tag,
    Ingredient,
    Favorite,
    CountIngredient,
    Cart
)


class RecipeIngredientInline(admin.TabularInline):
    model = CountIngredient
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CountIngredient)
class CountIngredientAdmin(admin.ModelAdmin):
    pass
