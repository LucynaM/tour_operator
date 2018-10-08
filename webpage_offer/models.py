from django.db import models
from tinymce.models import HTMLField

# Create your models here.


CATEGORIES = (
    ('school_trip', 'oferta dla szkół'),
    ('work_trip', 'oferta dla firm'),
    ('pilgrimage', 'pielgrzymka'),
)

class Offer(models.Model):
    """A class to represent offer"""
    title = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORIES, max_length=20)
    direction = models.CharField(max_length=255)
    duration_in_days = models.IntegerField()
    short_descr = models.TextField(max_length=200)
    schedule = HTMLField()
    price = models.FloatField(null=True, blank=True)
    #flags for selection in category
    selected = models.BooleanField(default=False)
    selected_sort = models.IntegerField(null=True, blank=True)
    #flags for recommendation choice
    recommended = models.BooleanField(default=False)
    recommended_sort = models.IntegerField(null=True, blank=True)
    # flag that allows admin to set an offer as "inactive"
    withdrawn = models.BooleanField(default=False)

    @property
    def name(self):
        return '{}: {}'.format(self.category, self.title)

    def __str__(self):
        return self.name

class Holiday(models.Model):
    """A class to represent holiday offer"""
    title = models.CharField(max_length=255)
    short_descr = models.TextField(max_length=200)
    schedule = HTMLField()

    def __str__(self):
        return self.title


