from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=120, blank=True)
    isbn = models.CharField(max_length=50, blank=True, null=True, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.available_copies}/{self.total_copies})"
