# Generated by Django 5.1.4 on 2024-12-07 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Имя персонажа')),
                ('personality', models.TextField(verbose_name='Характер персонажа')),
                ('photo', models.ImageField(upload_to='chatacters/', verbose_name='Фотография персонажа')),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=16, verbose_name='Кто написал сообщение')),
                ('message', models.TextField(verbose_name='Сообщение')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название истории')),
                ('description', models.TextField(verbose_name='Описание истории')),
                ('start_text', models.TextField(verbose_name='Вводный текст для пользователя')),
                ('photo', models.ImageField(upload_to='history/', verbose_name='Фотография для первого сообщения истории')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='historys', to='app.character', verbose_name='Персонаж этой истории')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=64, verbose_name='Id чата пользователя')),
                ('language', models.CharField(default='ru', max_length=4, verbose_name='Язык пользователя')),
                ('choose_history', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usrs', to='app.history', verbose_name='Выбранная история')),
                ('history_message', models.ManyToManyField(blank=True, to='app.text', verbose_name='История переписки')),
            ],
        ),
    ]
