import datetime
from rest_framework.test import APITestCase, APIClient
from mailing.models import Client, MailingList
from django.urls import reverse
from django.utils.timezone import make_aware

class MailingListViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        MailingList.objects.create(
            id='eecca42e-9572-44c4-9107-45b3554b2c6b',
            timestarted = make_aware(datetime.datetime.now()) + datetime.timedelta(seconds=1),
            timeended = make_aware(datetime.datetime.now()) + datetime.timedelta(seconds=3),
            message_text = 'This message text',
        )
        MailingList.objects.create(
            id='eecca42e-9572-44c4-9107-45b3554b2c62',
            timestarted = make_aware(datetime.datetime.now()) + datetime.timedelta(seconds=1),
            timeended = make_aware(datetime.datetime.now()) + datetime.timedelta(seconds=3),
            message_text = 'This message text 2',
        )
        Client.objects.create(
            id='eecca42e-9572-44c4-9107-45b3554b2c63',
            phone='79999682041',
            tag='python'
        )
        Client.objects.create(
            id='eecca42e-9572-44c4-9107-45b3554b2c64',
            phone='79999682042',
            tag='python'
        )
    
    def test_all_mailinglist(self):
        url = reverse('all')
        res = self.client.get(path=url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('max_message' in res.data[0].keys())
        self.assertTrue('total_accept' in res.data[0].keys())
    
    def test_create_mailinglist(self):
        url = reverse('new')
        data = {
            'timestarted': datetime.datetime.now() + datetime.timedelta(seconds=1),
            'timeended': datetime.datetime.now() + datetime.timedelta(seconds=3600),
            'message_text': 'This message text 1',
            'filtering': 'tag:python'
        }
        count_list = MailingList.objects.all().count()
        res = self.client.post(path=url, data=data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(MailingList.objects.all().count(), count_list+1)
    
    def test_single_mailinglist(self):
        url = reverse('single', kwargs={'pk': 'eecca42e-9572-44c4-9107-45b3554b2c6b'})
        res = self.client.get(path=url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('max_message' in res.data[0].keys())
        self.assertTrue('clients' in res.data[0].keys())
        self.assertTrue('total_accept' in res.data[0].keys())
    
    def test_single_not_found_mailinglist(self):
        url = reverse('single', kwargs={'pk': 'eecca42e-9572-44c4-9107-45b3554b2c60'})
        res = self.client.get(path=url)
        self.assertEqual(res.status_code, 404)

    def test_destroy_mailinglist(self):
        url = reverse('single', kwargs={'pk': 'eecca42e-9572-44c4-9107-45b3554b2c6b'})
        res = self.client.delete(path=url)
        self.assertEqual(res.status_code, 204)
    
    def test_update_mailinglist(self):
        url = reverse('single', kwargs={'pk': 'eecca42e-9572-44c4-9107-45b3554b2c6b'})
        data = {'message_text': 'This message text 2',
                'timestarted': make_aware(datetime.datetime.now()) + datetime.timedelta(seconds=1),
                'timeended': make_aware(datetime.datetime.now()) + datetime.timedelta(seconds=3)
                }
        res = self.client.put(path=url, data=data)
        self.assertEqual(MailingList.objects.get(id='eecca42e-9572-44c4-9107-45b3554b2c6b').message_text, 'This message text 2')
        self.assertEqual(res.status_code, 200)

class ClientViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        Client.objects.create(
            id='eecca42e-9572-44c4-9107-45b3554b2c61',
            phone='79999682041',
            tag='python'
        )
        Client.objects.create(
            id='eecca42e-9572-44c4-9107-45b3554b2c62',
            phone='79999682042',
            tag='python'
        )
    
    def test_all_client(self):
        url = reverse('all_client')
        res = self.client.get(path=url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(str(res.data[0]['id']), 'eecca42e-9572-44c4-9107-45b3554b2c61')
        self.assertEqual(str(res.data[1]['id']), 'eecca42e-9572-44c4-9107-45b3554b2c62')
    
    def test_create_client(self):
        url = reverse('new_client')
        data = {
            'phone': '79999682043',
            'tag': 'python1'
        }
        count_list = Client.objects.all().count()
        res = self.client.post(path=url, data=data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['phone_index'], '999')
        self.assertEqual(Client.objects.all().count(), count_list+1)
    
    def test_single_client(self):
        url = reverse('single_client', kwargs={'pk': 'eecca42e-9572-44c4-9107-45b3554b2c61'})
        res = self.client.get(path=url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(str(res.data['id']), 'eecca42e-9572-44c4-9107-45b3554b2c61')
    
    def test_single_not_found_client(self):
        url = reverse('single_client', kwargs={'pk': 'eecca42e-9572-44c4-9107-45b3554b2c60'})
        res = self.client.get(path=url)
        self.assertEqual(res.status_code, 404)

    def test_destroy_client(self):
        url = reverse('single_client', kwargs={'pk': 'eecca42e-9572-44c4-9107-45b3554b2c61'})
        count_list = Client.objects.all().count()
        res = self.client.delete(path=url)
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Client.objects.all().count(), count_list-1)

    def test_update_client(self):
        url = reverse('single_client', kwargs={'pk': 'eecca42e-9572-44c4-9107-45b3554b2c61'})
        data = {'phone_index': '443',
                'phone':'79999682041',
                'tag':'python'}
        res = self.client.put(path=url, data=data)
        self.assertEqual(Client.objects.get(id='eecca42e-9572-44c4-9107-45b3554b2c61').phone_index, '443')
        self.assertEqual(res.status_code, 200)
