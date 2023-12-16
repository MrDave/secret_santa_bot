from django.contrib import admin

from .models import Player, Game, Organizer


@admin.register(Organizer)
class UserAdmin(admin.ModelAdmin):
    search_fields = [
        'telegram_id',
    ]

    list_display = [
        'id',
        'telegram_id',
        
    ]


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'start_date',
        'end_date',
        'send_date',
    ]

    list_filter = [
        'name',
        'start_date',
        'end_date',
        'send_date',
    ]

    list_display = [
        'name',
        'organizer',
        'start_date',
        'end_date',
        'send_date',
        'link',
        'price_limit',
        'players_distributed',
    ]

    raw_id_fields = [
        'organizer',
    ]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    search_fields = [
        'telegram_id',
        'game',
        'name',
        'email',
    ]

    list_filter = [
        'telegram_id',
        'game',
        'name',
        'email',
    ]

    list_display = [
        'telegram_id',
        'game',
        'name',
        'email',
    ]
    raw_id_fields = [
        'avoided_players',
        'giftee',
    ]
