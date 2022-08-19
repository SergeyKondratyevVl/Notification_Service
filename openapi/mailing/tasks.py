from .services import get_clients, get_filters
from .models import MailingList, Message
from huey.contrib.djhuey import db_task, enqueue

@db_task()
def send_mail(mailinglist_id, filtering):
    filter_field, value = get_filters(filtering)
    clients = get_clients(filter_field, value)
    if clients:
        mailinglist = MailingList.objects.get(id=mailinglist_id)
        for client in clients:
            Message.objects.create(accepted=True,
                    message_mailinglist=mailinglist,
                    message_client = client)

            # Можно и bulk_create; вдруг не всем не отправят,
            # но тогда никому не отправят
        

@db_task()
def create_mailinglist(mailinglist_id, filtering=''):
    task = send_mail.s(mailinglist_id, filtering)
    result = enqueue(task)
        