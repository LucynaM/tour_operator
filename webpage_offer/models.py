from django.db import models
from tinymce.models import HTMLField

# Create your models here.


CATEGORIES = (
    ('for_school', 'oferta dla szkół'),
    ('for_work', 'oferta dla firm'),
    ('pilgrimage', 'pielgrzymka'),
)

class Offer(models.Model):
    """A class to represent offer"""
    title = models.CharField(max_length=255, verbose_name='Tytuł')
    category = models.CharField(choices=CATEGORIES, max_length=20, verbose_name='Kategoria')
    direction = models.TextField(max_length=600, verbose_name='Kierunki')
    duration_in_days = models.CharField(max_length=255, verbose_name='Czas trwania')
    short_descr = models.TextField(max_length=400, verbose_name='Krótki opis')
    schedule = models.TextField(verbose_name='Program')
    image = models.ImageField(upload_to='images', null=True, blank=True)
    #flags for selection in category
    selected = models.BooleanField(default=False)
    selected_sort = models.IntegerField(null=True, blank=True)
    #flags for recommendation choice
    recommended = models.BooleanField(default=False)
    recommended_sort = models.IntegerField(null=True, blank=True)
    # flag that allows admin to set an offer as "inactive"
    withdrawn = models.BooleanField(default=False, verbose_name='Wycofana z oferty')

    @property
    def name(self):
        return '{}: {}'.format(self.get_category_display(), self.title)

    def __str__(self):
        return self.name


class Holiday(models.Model):
    """A class to represent holiday offer"""
    title = models.CharField(max_length=255, verbose_name='Tytuł')
    direction = models.TextField(max_length=600, verbose_name='Kierunki', null=True, blank=True)
    duration_in_days = models.CharField(max_length=255, verbose_name='Czas trwania', null=True, blank=True)
    short_descr = models.TextField(max_length=400, verbose_name='Krótki opis', null=True, blank=True)
    schedule = models.TextField(verbose_name='Program')
    image = models.ImageField(upload_to='images', null=True, blank=True)
    withdrawn = models.BooleanField(default=False, verbose_name='Wycofana z oferty')

    def __str__(self):
        return self.title


class News(models.Model):
    """A class to represent news"""
    title = models.CharField(max_length=255, verbose_name='Tytuł')
    short_descr = models.TextField(max_length=200, verbose_name='Krótki opis', null=True, blank=True)
    entry = models.TextField(verbose_name='Wpis')
    entry_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.entry_date.strftime('%d.%m.%Y'), self.title)
