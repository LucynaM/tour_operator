from django.shortcuts import render, redirect
from django.views import View

from .models import Tour, TourParticipant, Participant
from .forms import TourForm, ParticipantForm

from datetime import datetime

# Create your views here.


class AddTour(View):
    def get(self, request):
        form = TourForm()
        tour_list = Tour.objects.all().exclude(end_date__lte=datetime.now().date())

        ctx = {
            'form': form,
            'tour_list': tour_list,
        }

        return render(request, 'webpage_tour/add_tour.html', ctx)

    def post(self, request):
        form = TourForm(request.POST)
        tour_list = Tour.objects.all().exclude(end_date__lte=datetime.now().date())

        if form.is_valid():
            tour = form.save()
            return redirect('tour: add_participant', pk=tour.pk)
        ctx = {
            'form': form,
            'tour_list': tour_list,
        }
        return render(request, 'webpage_tour/add_tour.html', ctx)



class AddParticipant(View):
    def get(self, request, pk):
        tour = Tour.objects.get(pk=pk)
        form = ParticipantForm()
        participants = tour.participants.all()
        ctx = {
            'tour': tour,
            'form': form,
            'participants': participants,
        }
        return render(request, 'webpage_tour/edit_tour.html', ctx)

    def post(self, request, pk):
        tour = Tour.objects.get(pk=pk)
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            TourParticipant.objects.create(tour=tour.pk, participant=participant.pk)
            form = ParticipantForm()
        participants = tour.participants.all()
        ctx = {
            'tour': tour,
            'form': form,
            'participants': participants,
        }
        return render(request, 'webpage_tour/edit_tour.html', ctx)