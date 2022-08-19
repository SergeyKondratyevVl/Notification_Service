from rest_framework import serializers
from .models import Client, MailingList

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'phone', 'phone_index', 'tag', 'time_zone')

class MailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = ('id', 'timestarted', 'message_text', 'timeended', 'filtering')
