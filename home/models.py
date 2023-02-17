from django.db import models


# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return self


class Newsletter(models.Model):
    newsletter_email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return self
