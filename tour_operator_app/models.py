from django.db import models

# Create your models here.

# Offer management - start

CATEGORIES = (
    ('pilgrimage', 'pielgrzymka'),
    ('school_trip', 'oferta dla szkół'),
    ('work_trip', 'oferta dla firm'),
    ('holiday', 'wakacje'),
)

class Offer(models.Model):
    """A class to represent offer"""
    title = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORIES, max_length=20)
    duration_in_days = models.IntegerField()
    short_descr = models.TextField(max_length=500)
    schedule = models.TextField()
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='images')
    #flags for selection in category
    selected = models.BooleanField(default=False)
    selected_sort = models.IntegerField(null=True, blank=True)
    #flags for recommendation choice
    recommended = models.BooleanField(default=False)
    recommended_sort = models.IntegerField(null=True, blank=True)
    # flags that allows set an offer as "inactive"
    withdrawn = models.BooleanField(default=False)

    @property
    def name(self):
        return '{}: {}'.format(self.category, self.title)

    def __str__(self):
        return self.name

# Offer management - stop


# Tour management models - start

class Tour(models.Model):
    """A class to represent tour as offer in time"""
    start_date = models.DateField()
    end_date = models.DateField()
    offer = models.ForeignKey(Offer, related_name='tours', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{}-{}: {}".format(self.start_date, self.end_date, self.offer)


class Participant(models.Model):
    """Basic data of a participant"""
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=30)
    phone = models.IntegerField()

    @property
    def name(self):
        return "{} {}".format(self.last_name, self.first_name)

    def __str__(self):
        return self.name


STATUSES = (
    ("reserved", "reserved"),
    ("confirmed", "confirmed"),
    ("cancelled", "cancelled"),
)


class TourParticipant(models.Model):
    """A class to represent participant of a tour"""
    participant = models.ForeignKey(Participant, related_name='participants', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, related_name='tours', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default='reserved', max_length=20)

    def __str__(self):
        return "{} {}".format(self.tour, self.participant)

# Tour management models - stop

# Blog management - start

class Entry(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()

# Blog management - stop
