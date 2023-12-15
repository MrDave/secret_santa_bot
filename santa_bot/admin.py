from django.contrib import admin

from .models import User, Game, Manage, UserAvoidance, Wishlist, ResultGame


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = [
        'username',
    ]

    list_display = [
        'telegram_id',
        'username',
        'email',
    ]


class ManageInline(admin.TabularInline):
    model = Manage
    extra = 0


class ResultGameInline(admin.TabularInline):
    model = ResultGame
    extra = 0


class UserAvoidanceInline(admin.TabularInline):
    model = UserAvoidance
    extra = 0


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]

    list_filter = [
        'name',
        'start_date',
        'end_date',
        'send_date',
    ]

    list_display = [
        'name',
        'user',
        'start_date',
        'end_date',
        'send_date',
        'link',
    ]
    raw_id_fields = [
        'user',
    ]

    inlines = [
        ManageInline,
        ResultGameInline,
        UserAvoidanceInline,
    ]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'game',
        'name',
        'price',

    ]
    raw_id_fields = [
        'user',
        'game',
    ]


@admin.register(UserAvoidance)
class UserAvoidanceAdmin(admin.ModelAdmin):
    list_display = [
        'game',
        'user',
        'avoided_user',

    ]
    raw_id_fields = [
        'game',
        'user',
        'avoided_user',
    ]

@admin.register(Manage)
class ManageAdmin(admin.ModelAdmin):
    list_display = [
        'game',
        'user',
        'is_manage',

    ]
    raw_id_fields = [
        'game',
        'user',
    ]


@admin.register(ResultGame)
class ResultGameAdmin(admin.ModelAdmin):
    list_display = [
        'game',
        'giver',
        'receiver',

    ]
    raw_id_fields = [
        'game',
        'giver',
        'receiver',
    ]