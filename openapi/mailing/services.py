from .models import Client

def get_clients(filter_field, value):
    if filter_field == 'tag':
        return Client.objects.filter(tag=value)
    elif filter_field == 'phone_index':
        return Client.objects.filter(phone_index=value)
    else:
        return []

def get_filters(filtering):
    return filtering.split(':')[0], filtering.split(':')[1]