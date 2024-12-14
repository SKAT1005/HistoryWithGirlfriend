from django.db import models

class User(models.Model):
    chat_id = models.CharField(max_length=64, verbose_name='Id чата пользователя')
    language = models.CharField(max_length=4, default='ru', verbose_name='Язык пользователя')
    choose_history = models.ForeignKey('History', blank=True, null=True, on_delete=models.PROTECT, related_name='usrs', verbose_name='Выбранная история')
    history_message = models.ManyToManyField('Text', blank=True, verbose_name='История переписки')

class Character(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя персонажа')
    personality = models.TextField(verbose_name='Характер персонажа')
    photo = models.ImageField(upload_to='chatacters/', verbose_name='Фотография персонажа')

    def __str__(self):
        return self.name


class History(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название истории')
    description = models.TextField(verbose_name='Описание истории')
    prompt = models.TextField(verbose_name='Промт истрории для персонажа')
    start_text = models.TextField(verbose_name='Вводный текст для пользователя')
    photo = models.ImageField(upload_to='history/', verbose_name='Фотография для первого сообщения истории')
    character = models.ForeignKey('Character', on_delete=models.PROTECT, related_name='historys',
                                  verbose_name='Персонаж этой истории')

class Text(models.Model):
    role = models.CharField(max_length=16, verbose_name='Кто написал сообщение')
    message = models.TextField(verbose_name='Сообщение')
