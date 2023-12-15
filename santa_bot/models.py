import uuid

from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(UUIDMixin, TimeStampedMixin):
    telegram_id = models.IntegerField(
        unique=True,
        default=False,
        blank=True,
        verbose_name='ID в телеграмме'
    )

    username = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name='Аккаунт в телеграмме'
    )

    email = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        verbose_name='Email',
    )

    # is_admin = models.BooleanField(
    #     default=False,
    #     null=True,
    #     blank=True,
    #     verbose_name='Администратор'
    # )

    def __str__(self):
        if self.username:
            return f'@{self.username}'
        else:
            return f'{self.telegram_id}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Game(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь',
        related_name='user'
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

    def __str__(self):
        return f'@{self.name}'

    class Meta:
        verbose_name = 'Розыгрыш'
        verbose_name_plural = 'Розыгрыши'


class Manage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        verbose_name='Пользователь',
        related_name='manage'
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        verbose_name='Розыгрыш',
        related_name='manage'
    )

    is_manage = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Управление'
    )

    def __str__(self):
        return f'{self.user.username} - {self.game.name}'

    class Meta:
        verbose_name = 'Управление'
        verbose_name_plural = 'Управления'


class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        verbose_name='Пользователь',
        related_name='wishlist'
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        verbose_name='Розыгрыш',
        related_name='wishlist'
    )

    name = models.CharField(
        max_length=200,
        # null=True,
        # blank=True,
        verbose_name='Название'
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'


class UserAvoidance(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        verbose_name='Розыгрыш',
        related_name='avoided_user'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь 1',
        related_name='avoiding_user'
    )
    avoided_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь 2',
        related_name='avoided_user'
    )

    def __str__(self):
        return f"{self.user.username} avoids {self.avoided_user.username}"

    class Meta:
        verbose_name = 'НЕ дружат'
        verbose_name_plural = 'НЕ дружат'


class ResultGame(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
        verbose_name='Розыгрыш',
        related_name='resultgame'
    )
    giver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Даритель',
        related_name='giver'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Получатель',
        related_name='receiver'
    )

    def __str__(self):
        return f"{self.giver.username} to {self.receiver.username}"

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
