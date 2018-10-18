from django.db import models
from webpage_offer.models import Offer

# Create your models here.

class Tour(models.Model):
    """A class to represent tour as an offer in time"""
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
    participant = models.ForeignKey(Participant, related_name='tours', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, related_name='participants', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default='reserved', max_length=20)

    def __str__(self):
        return "{} {}".format(self.tour, self.participant)
