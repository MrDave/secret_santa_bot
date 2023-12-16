from django.db import models


class Organizer(models.Model):
    telegram_id = models.IntegerField(
        unique=True,
        verbose_name='ID в телеграмме'
    )

    def __str__(self):
        return f'@{self.telegram_id}'

    class Meta:
        verbose_name = 'Организатор'
        verbose_name_plural = 'Организаторы'


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

    price_limit = models.CharField(
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
        verbose_name='Дата отправки подарков'
    )

    link = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Ссылка на розыгрыш'
    )

    players_distributed = models.BooleanField(
        verbose_name='Распределено?'
    )

    def __str__(self):
        return f'@{self.name}'

    class Meta:
        verbose_name = 'Розыгрыш'
        verbose_name_plural = 'Розыгрыши'


class Player(models.Model):
    telegram_id = models.IntegerField(
        verbose_name='telegram ID'
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='Розыгрыш',
        related_name='players'
    )

    name = models.CharField(
        max_length=50,
        verbose_name='имя'
    )

    # TODO: validate data and change CharField to EmailField
    email = models.CharField(
        max_length=254,
        verbose_name='email',
    )

    wishlist = models.TextField(
        null=True,
        blank=True,
        verbose_name='подарки'
    )

    avoided_players = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name='избегаемые игроки'
    )

    giftee = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Кому дарит',
        related_name='santa'
    )

    def __str__(self):
        return f'{self.telegram_id}'

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'
