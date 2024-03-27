from django.db import models

# Create your models here.


class Solution(models.Model):
    disease_name = models.CharField(max_length=255, null=True, blank=True)
    solution = models.CharField(max_length=1055, null=True, blank=True)
    medicine_recommended = models.CharField(max_length=255, null=True, blank=True)
    cause = models.CharField(max_length=1055, null=True, blank=True)