import uuid

from django.db import models
from datetime import date



class VirtualMachine(models.Model):

    OS_CHOICES = (
        ('US', 'Ubuntu Server'),
        ('WS', 'Windows Server'),
        ('DB11', 'Debian 11'),
        ('OL', 'Oracle Linux'),
    )

    PLATFORM_CHOICES = (
        ('AZ', 'Azure'),
        ('AWS', 'AWS (Amazon Web Services)'),
        ('GCP', 'Google Cloud Platform'),
        ('VMW', 'VMware'),
    )

    name = models.CharField(max_length=200)
    platform = models.CharField(choices=PLATFORM_CHOICES, max_length=3)  # Use the PLATFORM_CHOICES here
    os = models.CharField(choices=OS_CHOICES, max_length=100)
    creation_date = models.DateTimeField(null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    pgs_uuid = models.UUIDField(editable=False, default=uuid.uuid4, blank=True)
    def __str__(self):
        return f"{self.name}-{self.platform}"

