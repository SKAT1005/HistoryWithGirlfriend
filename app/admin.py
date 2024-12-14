from django.contrib import admin
from .models import History, Character, User, Text


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(User)
class CharacterAdmin(admin.ModelAdmin):
    pass


@admin.register(Text)
class CharacterAdmin(admin.ModelAdmin):
    pass