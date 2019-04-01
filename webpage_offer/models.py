from django.db import models

# Create your models here.


CATEGORIES = (
    ('for_school', 'oferta dla szkół'),
    ('for_work', 'oferta dla firm'),
    ('pilgrimage', 'pielgrzymka'),
    ('holiday', 'wakacje'),
)

class Offer(models.Model):
    """A class to represent offer"""
    title = models.CharField(max_length=255, verbose_name='Tytuł')
    category = models.CharField(choices=CATEGORIES, max_length=20, verbose_name='Kategoria')
    direction = models.TextField(max_length=600, verbose_name='Tagi')
    places = models.TextField(max_length=250, verbose_name='Miejsca', null=True, blank=True)
    duration_in_days = models.CharField(max_length=255, verbose_name='Czas trwania')
    short_descr = models.TextField(max_length=400, verbose_name='Krótki opis')
    descr = models.TextField(max_length=500, verbose_name='Opis dla wakacji', null=True, blank=True)
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


class News(models.Model):
    """A class to represent news"""
    title = models.CharField(max_length=255, verbose_name='Tytuł')
    short_descr = models.TextField(max_length=200, verbose_name='Krótki opis', null=True, blank=True)
    entry = models.TextField(verbose_name='Wpis')
    entry_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.entry_date.strftime('%d.%m.%Y'), self.title)
