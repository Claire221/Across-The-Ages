from django.db import models


# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=20, null=True, blank=False)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=False)
    message = models.TextField(null=True, blank=False)

    def __str__(self):
        return self


class Newsletter(models.Model):
    email = models.CharField(max_length=30, null=True, blank=False)

    def __str__(self):
        return self
