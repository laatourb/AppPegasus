from django.contrib import admin
from django.urls import path, include
from Formulaire.views import create_vm, virtualmachine_detail


app_name = 'vm'

urlpatterns = [
    path('add/', create_vm, name = 'vm-add'),
    path('machineinfo/', virtualmachine_detail, name='vm-info')
]