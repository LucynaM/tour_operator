from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Tour, TourParticipant, Participant, STATUSES
from .forms import TourForm, ParticipantForm, TourParticipantForm

from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


# Create your views here.

def get_dates(start, end):
    # format dates range
    if start.year == end.year and start.month == end.month:
        start = start.strftime('%d.')
    elif start.year == end.year:
        start = start.strftime('%d.%m.')
    else:
        start = start.strftime('%d.%m.%Y')
    end = end.strftime('%d.%m.%Y')
    date = ('{}-{}'.format(start, end))
    return date


def format_phone(phone):
    phone = str(phone)
    j = len(phone)
    new_phone = ""
    for i in phone[::-3]:
        z = phone[j-3:j]
        new_phone = " {}{}".format(z, new_phone)
        j -= 3
    return new_phone.strip()


class AddTour(LoginRequiredMixin, View):
    def get_tour_list(self):
        tour_list = Tour.objects.all().exclude(end_date__lte=datetime.now().date()).order_by('start_date')
        for tour in tour_list:
            tour.date = get_dates(tour.start_date, tour.end_date)
        return tour_list

    def get(self, request):
        form = TourForm()
        tour_list = self.get_tour_list()

        ctx = {
            'form': form,
            'tour_list': tour_list,
        }

        return render(request, 'webpage_tour/add_tour.html', ctx)

    def post(self, request):
        form = TourForm(request.POST)
        tour_list = self.get_tour_list()

        if form.is_valid():
            tour = form.save()
            return redirect('tour:add_participant', pk=tour.pk)

        ctx = {
            'form': form,
            'tour_list': tour_list,
        }
        return render(request, 'webpage_tour/add_tour.html', ctx)


class AddParticipant(LoginRequiredMixin, View):

    def get_tour(self, pk):
        tour = Tour.objects.get(pk=pk)
        tour.date = get_dates(tour.start_date, tour.end_date)
        return tour

    def get_tour_participants(self, obj):
        participants = obj.participants.all().order_by('-status', 'participant__last_name')
        for participant in participants:
            participant.participant.new_phone = format_phone(participant.participant.phone)
        return participants

    def get(self, request, pk):
        tour = self.get_tour(pk)
        form = ParticipantForm()
        participants = self.get_tour_participants(tour)

        ctx = {
            'tour': tour,
            'form': form,
            'participants': participants,
            'statuses': STATUSES,
        }
        return render(request, 'webpage_tour/add_participant.html', ctx)

    def post(self, request, pk):
        tour = self.get_tour(pk)
        form = ParticipantForm(request.POST)
        msg_err = ""

        if form.is_valid():
            # check if a person with already exists in db, if so - retrieve old one, if no - create a new one
            participant_list = Participant.objects.filter(**form.cleaned_data)
            if participant_list:
                participant = participant_list[0]
            else:
                participant = form.save()
            if not TourParticipant.objects.filter(tour=tour, participant=participant):
                TourParticipant.objects.create(tour=tour, participant=participant)
            else:
                msg_err = "This participant has already been added to the tour"

            form = ParticipantForm()

        participants = self.get_tour_participants(tour)

        ctx = {
            'tour': tour,
            'form': form,
            'participants': participants,
            'statuses': STATUSES,
            "msg_err": msg_err,
        }
        return render(request, 'webpage_tour/add_participant.html', ctx)


class EditTour(LoginRequiredMixin, View):

    def get_tour(self, pk):
        tour = Tour.objects.get(pk=pk)
        tour.date = get_dates(tour.start_date, tour.end_date)
        return tour

    def get(self, request, pk):
        tour = self.get_tour(pk)
        form = TourForm(instance=tour)

        ctx = {
            'tour': tour,
            'form': form,
        }

        return render(request, 'webpage_tour/edit_tour.html', ctx)

    def post(self, request, pk):
        tour = self.get_tour(pk)
        form = TourForm(request.POST, instance=tour)

        if form.is_valid():
            tour.save()
            return redirect('tour:add_participant', pk=tour.pk)
        ctx = {
            'tour': tour,
            'form': form,
        }
        return render(request, 'webpage_tour/add_tour.html', ctx)



class EditParticipant(LoginRequiredMixin, View):
    def get_participant(self, participant_pk):
        participant = Participant.objects.get(pk=participant_pk)
        participant.new_phone = format_phone(participant.phone)
        return participant

    def get(self, request, tour_pk, participant_pk):
        participant = self.get_participant(participant_pk)
        form = ParticipantForm(instance=participant)

        ctx = {
            'participant': participant,
            'form': form,
        }
        return render(request, 'webpage_tour/edit_participant.html', ctx)

    def post(self, request, tour_pk, participant_pk):
        participant = self.get_participant(participant_pk)
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


def generate_pdf(request, pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tour_participants.pdf"'

    pdfmetrics.registerFont(TTFont('Radjhani', 'webpage_offer/static/webpage_offer/fonts/Rajdhani-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('RadjhaniBd', 'webpage_offer/static/webpage_offer/fonts/Rajdhani-Bold.ttf'))

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4)
    p.translate(mm, mm)


    tour = Tour.objects.get(pk=pk)
    participants = tour.participants.all().order_by('-status', 'participant__last_name')
    for participant in participants:
        participant.participant.new_phone = format_phone(participant.participant.phone)

    # Draw things on the PDF.
    p.setFont('RadjhaniBd', 10)
    p.drawString(100, 775, "uczestnik")
    p.drawString(250, 775, "data urodzin")
    p.drawString(350, 775, "telefon")
    p.drawString(450, 775, "status")

    y = 750
    for participant in participants:
        p.setFont('Radjhani', 10)
        p.drawString(100, y, u"{}".format(participant.participant.name))
        p.drawString(250, y, u"{}".format(participant.participant.date_of_birth))
        p.drawString(350, y, u"{}".format(participant.participant.new_phone))
        p.drawString(450, y, u"{}".format(participant.status))
        y -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


class FillParticipant(LoginRequiredMixin, View):
    def get(self, request):
        if not 'firstName' in request.GET.keys() and not 'lastName' in request.GET.keys():
            try:
                participants = Participant.objects.all()
                data = {}
                data['names'] = []
                for participant in participants:
                    if not participant.last_name in data['names']:
                        data['names'].append(participant.last_name)
                return JsonResponse(data)
            except Exception as e:
                print(e)
        elif 'firstName' in request.GET.keys() and 'lastName' in request.GET.keys():
            try:
                last_name = request.GET['lastName']
                first_name = request.GET['firstName']
                participants = Participant.objects.filter(last_name=last_name, first_name=first_name)
                data = {}
                data['phones'], data['dates_of_birth'] = [], []

                for participant in participants:
                    if not participant.phone in data['phones']:
                        data['phones'].append(participant.phone)
                    if not participant.date_of_birth in data['dates_of_birth']:
                        data['dates_of_birth'].append(participant.date_of_birth)
                return JsonResponse(data)
            except Exception as e:
                print(e)