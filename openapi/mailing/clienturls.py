from django.urls import path
from .views import ClientApi

urlpatterns = [
    path('', ClientApi.as_view({'get': 'list'}), 
        name='all_client'),
    
    path('new/', ClientApi.as_view({'post': 'create'}), 
        name='new_client'),
    
    path('<str:pk>/', ClientApi.as_view({'get': 'retrieve',
                                            'delete': 'destroy',
                                            'put': 'update'}), 
        name='single_client'),
    
]