from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views import View
from .models import Tour, TourParticipant, Participant, STATUSES
from .forms import TourForm, ParticipantForm
from webpage_offer.views import AdminUserPassesTestMixin

from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

import xlsxwriter

# Create your views here.

def get_dates(start, end):
    """format dates range"""
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
    """format input phone as 'XXX XXX XXX'"""
    phone = str(phone)
    break_point = len(phone) % 3
    start = phone[0:break_point]
    end = phone[break_point::]
    phone_end = " ".join(end[i:i+3] for i in range(0,len(end),3) ).strip()
    return '{} {}'.format(start, phone_end) if start else phone_end


class AddTour(AdminUserPassesTestMixin, View):
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


class AddParticipant(AdminUserPassesTestMixin, View):
    @staticmethod
    def get_tour(pk):
        tour = Tour.objects.get(pk=pk)
        tour.date = get_dates(tour.start_date, tour.end_date)
        return tour

    @staticmethod
    def get_tour_participants(obj):
        participants = obj.participants.all().order_by('-status', 'participant__last_name')
        for participant in participants:
            participant.participant.new_phone = format_phone(participant.participant.phone)
        return participants

    def get(self, request, pk):
        tour = self.get_tour(pk)
        form = ParticipantForm()

        ctx = {
            'tour': tour,
            'form': form,
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
                return redirect('tour:edit_tour', pk=tour.pk)
            else:
                msg_err = "This participant has already been added to the tour"

        ctx = {
            'tour': tour,
            'form': form,
            "msg_err": msg_err,
        }
        return render(request, 'webpage_tour/add_participant.html', ctx)


class EditTour(AdminUserPassesTestMixin, View):
    @staticmethod
    def get_tour(pk):
        tour = Tour.objects.get(pk=pk)
        tour.date = get_dates(tour.start_date, tour.end_date)
        return tour

    @staticmethod
    def get_tour_participants(obj):
        participants = obj.participants.all().order_by('-status', 'participant__last_name')
        for participant in participants:
            participant.participant.new_phone = format_phone(participant.participant.phone)
        return participants

    def get(self, request, pk):

        tour = self.get_tour(pk)
        participants = self.get_tour_participants(tour)
        form = TourForm(instance=tour)

        ctx = {
            'tour': tour,
            'form': form,
            'participants': participants,
            'statuses': STATUSES,
            'model': 'tour',
        }

        return render(request, 'webpage_tour/edit_tour.html', ctx)

    def post(self, request, pk):
        tour = self.get_tour(pk)
        form = TourForm(request.POST, instance=tour)

        if form.is_valid():
            form.save()

        tour = self.get_tour(pk)
        participants = self.get_tour_participants(tour)

        ctx = {
            'tour': tour,
            'form': form,
            'participants': participants,
            'statuses': STATUSES,
            'model': 'tour',
        }
        return render(request, 'webpage_tour/edit_tour.html', ctx)



class EditParticipant(AdminUserPassesTestMixin, View):
    def get_participant(self, participant_pk):
        participant = Participant.objects.get(pk=participant_pk)
        participant.new_phone = format_phone(participant.phone)
        return participant

    def get(self, request, tour_pk, participant_pk):
        participant = self.get_participant(participant_pk)
        tour = Tour.objects.get(pk=tour_pk)
        tour_participant = TourParticipant.objects.get(tour=tour, participant=participant)
        form = ParticipantForm(instance=participant)


        ctx = {
            'participant': participant,
            'form': form,
            'model': 'participant',
            'tour_participant': tour_participant
        }
        return render(request, 'webpage_tour/edit_participant.html', ctx)

    def post(self, request, tour_pk, participant_pk):
        participant = self.get_participant(participant_pk)
        tour = Tour.objects.get(pk=tour_pk)
        tour_participant = TourParticipant.objects.get(tour=tour, participant=participant)
        form = ParticipantForm(request.POST, instance=participant)

        if form.is_valid():
            form.save()
            return redirect('tour:add_participant', pk=tour_pk)

        ctx = {
            'participant': participant,
            'form': form,
            'model': 'participant',
            'tour_participant': tour_participant
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


def generate_xls(request, pk):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=tour_participants.xlsx"

    tour = Tour.objects.get(pk=pk)
    participants = tour.participants.all().order_by('-status', 'participant__last_name')

    for participant in participants:
        participant.new_phone = format_phone(participant.participant.phone)

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    bold = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet()

    header_col = 0
    for header in ['uczestnik', 'data urodzin', 'telefon', 'status']:
        worksheet.write(0, header_col, header, bold)
        header_col += 1

    participant_col = 0
    participant_row = 1
    for participant in participants:
        worksheet.write(participant_row, participant_col, participant.participant.name)
        worksheet.write(participant_row, participant_col + 1, participant.participant.date_of_birth)
        worksheet.write(participant_row, participant_col + 2, participant.new_phone)
        worksheet.write(participant_row, participant_col + 3, participant.status)
        participant_row += 1

    workbook.close()

    return response


class FillParticipant(View):
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


class DeleteItem(AdminUserPassesTestMixin, View):

    def get_item(self, model, pk):
        return Tour.objects.get(pk=pk) if model == "tour" else TourParticipant.objects.get(pk=pk)

    def get(self, request, model, pk):
        item = self.get_item(model, pk)
        ctx = {
            'item': item,
        }
        return render(request, 'webpage_tour/delete_item.html', ctx)

    def post(self, request, model, pk):
        item = self.get_item(model, pk)

        item.delete()
        if model == "participant":
            return redirect('tour:edit_tour', item.tour.pk)
        return redirect('tour:add_tour')