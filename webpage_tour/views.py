from django.shortcuts import render, redirect
from django.views import View
from django import forms
from django.http import JsonResponse, HttpResponseBadRequest

from .models import Tour, TourParticipant, Participant, STATUSES
from .forms import TourForm, ParticipantForm, TourParticipantForm

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
        tour_list = Tour.objects.all().exclude(end_date__lte=datetime.now().date()).order_by('start_date')

        if form.is_valid():
            tour = Tour.objects.create(**form.cleaned_data)
            return redirect('tour:add_participant', pk=tour.pk)
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
            'statuses': STATUSES,
        }
        return render(request, 'webpage_tour/add_participant.html', ctx)

    def post(self, request, pk):
        tour = Tour.objects.get(pk=pk)
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant_list = Participant.objects.filter(**form.cleaned_data)
            if participant_list:
                participant = participant_list[0]
            else:
                participant = form.save()
            TourParticipant.objects.create(tour=tour, participant=participant)
            form = ParticipantForm()
        participants = tour.participants.all()
        ctx = {
            'tour': tour,
            'form': form,
            'participants': participants,
        }
        return render(request, 'webpage_tour/add_participant.html', ctx)


class EditTour(View):
    def get(self, request, pk):
        tour = Tour.objects.get(pk=pk)
        form = TourForm(instance=tour)

        ctx = {
            'tour': tour,
            'form': form,
        }

        return render(request, 'webpage_tour/edit_tour.html', ctx)

    def post(self, request, pk):
        tour = Tour.objects.get(pk=pk)
        form = TourForm(request.POST, instance=tour)

        if form.is_valid():
            form.save()
            return redirect('tour:add_participant', pk=tour.pk)
        ctx = {
            'tour': tour,
            'form': form,
        }
        return render(request, 'webpage_tour/add_tour.html', ctx)


class EditParticipant(View):
    def get(self, request, tour_pk, participant_pk):
        participant = Participant.objects.get(pk=participant_pk)
        form = ParticipantForm(instance=participant)
        ctx = {
            'participant': participant,
            'form': form,
        }
        return render(request, 'webpage_tour/edit_participant.html', ctx)
    def post(self, request, tour_pk, participant_pk):
        participant = Participant.objects.get(pk=participant_pk)
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('tour:add_participant', pk=tour_pk)

        ctx = {
            'participant': participant,
            'form': form,
        }
        return render(request, 'webpage_tour/edit_participant.html', ctx)


class ChangeStatus(View):
    def get(self, request, pk):
        try:
            # pk z TourParticipant
            status = request.GET['status']
            tour_participant = TourParticipant.objects.get(pk=pk)
            tour_participant.status = status
            tour_participant.save()
            data = {
                'status': status,
            }
            return JsonResponse(data)
        except Exception as e:
            print(e)
            