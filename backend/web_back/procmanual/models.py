from django.db import models
from django.utils import timezone
import json

# Create your models here.
class Site(models.Model):
    site = models.CharField(max_length=200)

    def __str__(self):
        return self.site

class Rank(models.Model):
    rank = models.CharField(max_length=10)

    def __str__(self):
        return self.rank

class Procmanual(models.Model):
    title = models.CharField(max_length=200)

    site = models.ForeignKey(Site, related_name='procmanual', on_delete=models.CASCADE, blank=True, null=True)
    rank = models.ForeignKey(Rank, related_name='procmanual', on_delete=models.CASCADE, blank=True, null=True)

    created_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    check_cmd = models.JSONField(default=dict, blank=True)
    check_list = models.JSONField(default=dict, blank=True)
    execute_cmd = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title



