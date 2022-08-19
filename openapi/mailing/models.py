from django.db import models
import uuid
from django.core.validators import RegexValidator
from .attributes import TZone

class MailingList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    timestarted = models.DateTimeField(verbose_name='Время запуска рассылки')
    timeended = models.DateTimeField(verbose_name='Время окончания рассылки')
    message_text = models.TextField(max_length=1200, verbose_name='Текст сообщения')
    filtering = models.CharField(max_length=50, default='tag:python', verbose_name='Фильтр свойств клиентов')

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    phone_regex = RegexValidator(regex=r'7\d{10}', message="Длина = 11 знаков. Прим: 78005553535")
    phone = models.CharField(max_length=11, null=False, unique=True, validators=[phone_regex], verbose_name='Номер телефона клиента')
    phone_index = models.CharField(max_length=3, default='495', blank=True, verbose_name='Код мобильного оператора')
    tag = models.CharField(max_length=10, default='python', verbose_name='Тег')
    time_zone = models.CharField(max_length=30, choices=TZone, default='UTC', verbose_name='Часовой пояс')

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    timesended = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')
    accepted = models.BooleanField(default=False, verbose_name='Статус отправки')
    message_mailinglist = models.ForeignKey(to=MailingList, related_name='mailinglist_ref', on_delete=models.CASCADE, verbose_name='ID рассылки')
    message_client = models.ForeignKey(to=Client, related_name='client_ref', on_delete=models.CASCADE, verbose_name='ID клиента')
