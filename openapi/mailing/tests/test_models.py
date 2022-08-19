import datetime
from rest_framework.test import APITestCase
from mailing.models import MailingList, Client
from django.db.utils import IntegrityError
from django.db.transaction import TransactionManagementError
from django.utils.timezone import make_aware

class MailingListTest(APITestCase):

    def test_create_mailinglist(self):
        mailinglist = MailingList.objects.create(
            id='eecca42e-9572-44c4-9107-45b3554b2c6b',
            timestarted = make_aware(datetime.datetime.now()) + datetime.timedelta(hours=1),
            timeended = make_aware(datetime.datetime.now()) + datetime.timedelta(hours=2),
            message_text = 'This message text',
        )
        self.assertEqual(mailinglist.message_text, 'This message text')
        with self.assertRaises(IntegrityError):
            MailingList.objects.create(id='eecca42e-9572-44c4-9107-45b3554b2c6b',
                                       timestarted = make_aware(datetime.datetime.now()) + datetime.timedelta(hours=3),
                                       timeended = make_aware(datetime.datetime.now()) + datetime.timedelta(hours=4),
                                       message_text = 'This message text 1',
                                    )

class ClientTest(APITestCase):
    def test_create_client(self):
        client = Client.objects.create(
            id='eecca42e-9572-44c4-9107-45b3554b2c61',
            phone='79999682041',
            tag='python',
            phone_index = '999'
        )
        self.assertEqual(client.tag, 'python')
        self.assertEqual(client.phone, '79999682041')
        self.assertEqual(client.phone_index, '999')

        with self.assertRaises(IntegrityError):
            Client.objects.create(
                id='eecca42e-9572-44c4-9107-45b3554b2c6b',
                phone='79999682041',
                tag='python'
            )
        
        with self.assertRaises(TransactionManagementError):
            Client.objects.create(
                id='eecca42e-9572-44c4-9107-45b3554b2c61',
                phone='79999682042',
                tag='python'
            )
    
    def test_create_default_client(self):
        client = Client.objects.create(phone='78005553535')
        self.assertEqual(client.phone_index, '495')
        self.assertEqual(client.tag, 'python')
        self.assertEqual(client.phone, '78005553535')
