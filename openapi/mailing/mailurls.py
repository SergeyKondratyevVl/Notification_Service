from django.urls import path
from .views import MailingListApi

urlpatterns = [
    path('', MailingListApi.as_view({'get': 'list'}), 
        name='all'),

    path('new/', MailingListApi.as_view({'post': 'create'}), 
        name='new'),
    
    path('<str:pk>/', MailingListApi.as_view({'get': 'retrieve',
                                            'delete': 'destroy',
                                            'put': 'update'}), 
        name='single'),
    
]