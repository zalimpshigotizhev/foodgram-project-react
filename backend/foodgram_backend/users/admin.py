from django.contrib import admin
from .models import (
    Subscribe,
    CustomUser
)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    ...


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    ...
