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
    # body = models.TextField()

    site = models.ForeignKey(Site, related_name='procmanual', on_delete=models.CASCADE, blank=True, null=True)
    rank = models.ForeignKey(Rank, related_name='procmanual', on_delete=models.CASCADE, blank=True, null=True)

    # check_cmd = models.JSONField(default=list)

    created_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    


