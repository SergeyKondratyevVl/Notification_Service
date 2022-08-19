from rest_framework.viewsets import ModelViewSet
from .services import get_filters
from .tasks import create_mailinglist
from .serializers import ClientSerializer, MailingListSerializer
from .models import Client, MailingList, Message
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Count, Case, When
from dateutil.parser import parse
from django.utils.timezone import make_aware

class MailingListApi(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer

    @transaction.atomic(using='default')
    def create(self, request, *args, **kwargs):
        data = {}
        data['timestarted'] = make_aware(parse(request.data['timestarted']))
        data['timeended'] = make_aware(parse(request.data['timeended']))
        data['message_text'] = request.data['message_text']
        data['filtering'] = request.data['filtering']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        mailinglist = MailingList.objects.create(**data)
        create_mailinglist.schedule((str(mailinglist.id), request.data['filtering']),
                                    eta=data['timestarted'], 
                                    expires=data['timeended'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = Message.objects.all()\
            .aggregate(total_accept=Count(Case(When(accepted=True, then=1))))
        data['max_message'] = Client.objects.all().count() * MailingList.objects.all().count()
        return Response(data=(data, serializer.data), status=200)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        id = serializer.data['id']
        data = Message.objects.filter(message_mailinglist=id)\
                    .aggregate(total_accept=Count(Case(When(accepted=True, then=1))))
        data['clients'] = Message.objects.filter(message_mailinglist=id,
                                message_client__tag = get_filters(serializer.data['filtering'])[1])\
                                .count()
        data['max_message'] = Client.objects.all().count()
        return Response(data=(data, serializer.data), status=200)

class ClientApi(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        data = {}
        data['phone'] = request.data['phone']
        data['tag'] = request.data['tag']
        data['time_zone'] = request.data['time_zone']
        data['phone_index'] = request.data['phone'][1:4]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    