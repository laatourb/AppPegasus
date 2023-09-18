from django import forms
from .models import VirtualMachine 
from django.core.exceptions import ValidationError 

class VirtualMachineForm(forms.ModelForm):
   class Meta:
      model = VirtualMachine
      fields = (
         'name',  
         'os', 
         'platform'
      )

          
        
