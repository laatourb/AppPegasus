from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from .models import VirtualMachine 
from django.views.generic import FormView
from .forms import VirtualMachineForm
from django.contrib import messages
from .serializer import VirtualMachineSerializer
from rest_framework.renderers import JSONRenderer 
from datetime import datetime
import json
import os 
import requests


def call_AWX(data):
    awx_api_url = settings.AWX_API_URL
    token = settings.AWX_API_TOKEN
    JOB_TEMPLATE_ID = settings.AWX_JOB_ID

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    data_for_post = {
        "name": "JobAzureTemplate",
        "playbook": settings.AWX_JOB_NAME,
        "ask_variables_on_launch": True,
        "extra_vars": data
    }

    job_template_url = f"{awx_api_url}/job_templates/{JOB_TEMPLATE_ID}/launch/"
    response = requests.post(job_template_url, json=data_for_post, headers=headers)

    if response.status_code == 201:
        print("Requête POST réussie.")
        print(response.json())
    else:
        print(f"Erreur lors de la requête POST. Code d'état : {response.status_code}")
        print(response.text)

# Create function for validation of form with message of success
def create_vm(request):
    template_name = 'Formulaire/main.html'
    title = "Demande de VM"
    context = {}

    if request.method == 'POST': #if the form has been submitted...
        form = VirtualMachineForm(request.POST) #A form bound to the POST data
        if form.is_valid(): #condition de formulaire
            VirtualMachine = form.save() #save form in a variable
            
            #declaring variable which we need for the JSON file
            vm_name = VirtualMachine.name
            request_date = datetime.now().strftime("%Y-%m-%d")  # Format data: YYYY-MM-DD HH-MM-SS
            vm_os = VirtualMachine.os
            type_of_platform = VirtualMachine.platform
            
            #variable to give the path where we want to store the files
            directory_path = "/home/bilalflowline/projets/Application/PegasusProject/Pegasus/Formulaire/json"  # Replace this with the path to your folder
            
            #check the path
            os.makedirs(directory_path, exist_ok=True)
            
            #variable to name the file
            file_name = f"{vm_name}_{request_date}.json"

            # variable for join path without error and file name
            file_path = os.path.join(directory_path, file_name)
            
            # stock the data in a dictionnary
            data = {
                "vm_name": vm_name,
                "vm_size": "Standard_B1s",
                "vm_image": "Canonical:UbuntuServer:18.04-LTS:latest",
                "vm_username": "testansibleuser",
                "vm_password": "my-password@1234",
                "rg_name": "PERSO_BILAL",
                "vnet_name": "vnet-ansible",
                "subnet_name": "subnet-ansible",
                "location": "westeurope",
                "offer": "UbuntuServer",
                "publisher": "Canonical",
                "sku": "18.04-LTS",
                "version": "latest"
            }
            
            # Write the data as JSON to the file
            with open(file_path, 'w') as file:
                json.dump(data, file)


            # Use the call_AWX function to input JSON to AWX
            call_AWX(data)

            # success message and file redirection
            messages.success(request, 'Successfully saved the VM creation request')  # Save success message
            return HttpResponseRedirect(reverse('vm:vm-add'))
    else:
        form = VirtualMachineForm()

    context['form'] = form
    context['title'] = title


    return render(request,
                 template_name,
                 context) 




# def call_AWX(data):
#     awx_api_url = settings.AWX_API_URL
#     token = settings.AWX_API_TOKEN
#     JOB_TEMPLATE_ID = settings.AWX_TERRAFORM_JOB_ID

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {token}"
#     }

#     data_for_post = {
#         "name": "JobAzureTemplate",
#         "playbook": "Azure/create_vm_job_template.yml",
#         "ask_variables_on_launch": True,
#         "extra_vars": data
#     }

#     job_template_url = f"{awx_api_url}/job_templates/{JOB_TEMPLATE_ID}/launch/"
#     response = requests.post(job_template_url, json=data_for_post, headers=headers)

#     if response.status_code == 200:
#         print("Requête POST réussie.")
#         print(response.json())
#     else:
#         print(f"Erreur lors de la requête POST. Code d'état : {response.status_code}")
#         print(response.text)

# def create_vm(request):
#     template_name = 'Formulaire/main.html'
#     title = "Demande de VM"
#     context = {}

#     if request.method == 'POST':
#         form = VirtualMachineForm(request.POST)

#         if form.is_valid():
#             virtual_machine = form.save()

#             vm_name = virtual_machine.name
#             request_date = datetime.now().strftime("%Y-%m-%d")
#             # Altri dati necessari per il JSON finale
#             data = {
#                 "vm_name": vm_name,
#                 "vm_size": "Standard_B1s",
#                 # Altri campi
#             }

#             directory_path = "/percorso/al/file.json"
#             os.makedirs(directory_path, exist_ok=True)
#             file_name = f"{vm_name}_{request_date}.json"
#             file_path = os.path.join(directory_path, file_name)

#             with open(file_path, 'w') as file:
#                 json.dump(data, file)

#             # Chiama la funzione call_AWX per inviare il JSON a AWX
#             call_AWX(data)

#             # Messaggio di successo e reindirizzamento
#             messages.success(request, 'Successfully saved the VM creation request')
#             return HttpResponseRedirect(reverse('vm:vm-add'))
#     else:
#         form = VirtualMachineForm()

#     context['form'] = form
#     context['title'] = title

#     return render(request, template_name, context)



















# def send_json_to_awx(file_path):  
#     # Fetch the token from somewhere (e.g., from environment variable) and set it here
#     token = "uobkNOXR0w8Pb31wbpMnuhFmMHtp8D"  # Replace with your actual AWX API token
#     awx_api_url = "http://20.160.46.17:31368/api/v2/"  # Replace with the actual AWX API URL

#     # Create the header with the authentication token
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }

#     # Load the JSON data from the file
#     with open(file_path, 'r') as file:
#         json_data = json.load(file)

#     # Send the JSON data to AWX API using a POST request
#     try:
#         response = requests.post(awx_api_url, json=json_data, headers=headers)

#         # Check the response status
#         if response.status_code == 200:
#             print("Data sent successfully to AWX API.")
#         else:
#             print(f"Error while sending data to AWX API. Status code: {response.status_code}")
#             print(response.text)
#     except requests.exceptions.RequestException as e:
#         print(f"HTTP Request Error: {e}")

# def main():
#     # Variable to give the path where we want to store the files
#     directory_path = "/home/bilalflowline/projets/Application/PegasusProject/Pegasus/Formulaire/json"

#     # Check the path
#     os.makedirs(directory_path, exist_ok=True)

#     # Fetch the list of JSON files in the directory
#     json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

#     # Loop through each JSON file and send it to AWX API
#     for file in json_files:
#         file_path = os.path.join(directory_path, file)
#         send_json_to_awx(file_path)

# if __name__ == "__main__":
#     main()


# # Creating function for fetch data and transform in json format with serializer
 
def virtualmachine_detail(request):
    machines = VirtualMachine.objects.all()  # Get all Virtual Machine objects from the database
    serializer = VirtualMachineSerializer(machines, many=True)  # Pass many=True since we have multiple objects
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data, content_type='application/json')















# Create your views here.

# class MyVirtualMachineFormView(FormView):
#     form_class = VirtualMachineForm
#     template_name = 'Formulaire/main.html'

#     def get_success_url(self):
#         return self.request.path
    
#     def form_valid(self, form):
#         form.save()
#         messages.add_message(self.request, messages.INFO,'Enregistré avec succes la demande de creation de VM')
#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         return super().form_invalid(form)
    
#     def form_invalid(self, form):
#         form.add_error(None, 'Ups..... quelquechose ne va pas')
#         return super().form_invalid(form)
    

# messages.add_message(request, messages.INFO, 'Successfully saved the VM creation request')
#             return  HttpResponseRedirect(reverse('create-vm', kwargs={'id': VirtualMachine.id}))