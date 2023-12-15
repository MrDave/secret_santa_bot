from django.db import models


class Organizer(models.Model):
    telegram_id = models.IntegerField(
        unique=True,
        default=False,
        verbose_name='ID в телеграмме'
    )


class Game(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Организатор',
        related_name='organizer'
    )

    price_limit = name = models.CharField(
        max_length=200,
        verbose_name='Стоимость'
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата начала'
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата окончания'
    )

    send_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата розыгрыша'
    )

    link = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Ссылка на розыгрыш'
    )

    players_distributed = models.BooleanField(
        verbose_name='Распределено'
    )

    def __str__(self):
        return f'@{self.name}'

    class Meta:
        verbose_name = 'Розыгрыш'
        verbose_name_plural = 'Розыгрыши'


class Player(models.Model):
    telegram_id = models.IntegerField(
        unique=True,
        default=False,
        blank=True,
        verbose_name='ID в телеграмме'
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Розыгрыш',
        related_name='players'
    )

    name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name='Имя'
    )

    email = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        verbose_name='Email',
    )

    wishlist = models.TextField(
        null=True,
        blank=True,
        verbose_name='Подарки'
    )

    avoided_players = models.ManyToManyField(
        'self',
        verbose_name='Не дружит'
    )

    giftee = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Кому дарит',
        related_name='giftee'
    )

    def __str__(self):
        if self.username:
            return f'@{self.name}'
        else:
            return f'{self.telegram_id}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
