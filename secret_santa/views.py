from django.shortcuts import render
from django.shortcuts import get_object_or_404
from santa_bot.models import Game, Player
import random


def allocation(request, game_id):

    game = get_object_or_404(Game, pk=game_id)

    players = game.players.all()

    giftees = []

    for player in players:
        avoided_players = player.avoided_players.all()

        can_giftee = players.exclude(telegram_id=player.telegram_id).exclude(telegram_id__in=avoided_players).exclude(telegram_id__in=giftees)

        if can_giftee:
            transferee = random.choice(can_giftee)
            player.giftee = transferee
            player.save()
            giftees.append(transferee.telegram_id)

    game.players_distributed = True
    game.save()

    context = {
        'players': players,
        'game': game
    }

    return render(request, 'random.html', context)


def del_allocation(request, game_id):

    game = get_object_or_404(Game, pk=game_id)

    players = game.players.all()

    for player in players:
        player.giftee = None
        player.save()

    game.players_distributed = False
    game.save()

    return render(request, 'index.html')


def show_start(request, telegram_id):

    player = get_object_or_404(Player, pk=telegram_id)

    context = {
        'player': player,
        'giftee': player.giftee
    }

    return render(request, 'index.html', context)