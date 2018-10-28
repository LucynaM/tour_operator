from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views import View

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
    # get dates range for search form
    if start.year == end.year and start.month == end.month:
        start = start.strftime('%d.')
    elif start.year == end.year:
        start = start.strftime('%d.%m.')
    else:
        start = start.strftime('%d.%m.%Y')
    end = end.strftime('%d.%m.%Y')
    date = ('{}-{}'.format(start, end))
    return date


class AddTour(View):
    def get(self, request):
        form = TourForm()
        tour_list = Tour.objects.all().exclude(end_date__lte=datetime.now().date()).order_by('start_date')
        for tour in tour_list:
            tour.date = get_dates(tour.start_date, tour.end_date)

        ctx = {
            'form': form,
            'tour_list': tour_list,
        }

        return render(request, 'webpage_tour/add_tour.html', ctx)

    def post(self, request):
        form = TourForm(request.POST)
        tour_list = Tour.objects.all().exclude(end_date__lte=datetime.now().date()).order_by('start_date')
        for tour in tour_list:
            tour.date = get_dates(tour.start_date, tour.end_date)

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
        tour.date = get_dates(tour.start_date, tour.end_date)

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
        tour.date = get_dates(tour.start_date, tour.end_date)

        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant_list = Participant.objects.filter(**form.cleaned_data)
            if participant_list:
                participant = participant_list[0]
            else:
                participant = form.save()
            if not TourParticipant.objects.filter(tour=tour, participant=participant):
                TourParticipant.objects.create(tour=tour, participant=participant)
            form = ParticipantForm()
        participants = tour.participants.all()
        ctx = {
            'tour': tour,
            'form': form,
            'participants': participants,
            'statuses': STATUSES,
        }
        return render(request, 'webpage_tour/add_participant.html', ctx)


class EditTour(View):
    def get(self, request, pk):
        tour = Tour.objects.get(pk=pk)
        tour.date = get_dates(tour.start_date, tour.end_date)

        form = TourForm(initial={'offer': tour.offer,
                                 'start_date': tour.start_date.strftime('%d.%m.%Y'),
                                 'end_date': tour.end_date.strftime('%d.%m.%Y'),
                                 })
        #form = TourForm(instance=tour)

        ctx = {
            'tour': tour,
            'form': form,
        }

        return render(request, 'webpage_tour/edit_tour.html', ctx)

    def post(self, request, pk):
        tour = Tour.objects.get(pk=pk)
        tour.date = get_dates(tour.start_date, tour.end_date)

        form = TourForm(request.POST)

        if form.is_valid():
            Tour.objects.filter(pk=pk).update(**form.cleaned_data)
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


def generate_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    pdfmetrics.registerFont(TTFont('Theano', 'webpage_offer/static/webpage_offer/fonts/TheanoOldStyle-Regular.ttf'))

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4)
    p.translate(mm, mm)
    p.setFont('Theano', 10)

    # Draw things on the PDF.
    tour = Tour.objects.get(pk=5)
    participants = tour.participants.all().order_by('status', 'participant__last_name')
    y = 750
    for participant in participants:
        p.drawString(100, y, u"{}".format(participant.participant.name))
        p.drawString(250, y, u"tel:{}".format(participant.participant.phone))
        p.drawString(350, y, u"{}".format(participant.status))
        y -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return redirect('tour:add_tour')


class FillParticipant(View):
    def get(self, request):
        try:
            participants = Participant.objects.all()
            data = []
            for participant in participants:
                participant_dict = {}
                for key, value in participant.__dict__.items():
                    if key != '_state':
                        participant_dict[key] = value
                data.append(participant_dict)

            return JsonResponse(participants, safe=False)
        except Exception as e:
            print(e)


class SortParticipants(View):

    def get(self, request, pk):
        try:
            if 'key' in request.GET.keys():
                tour = Tour.objects.get(pk=pk)
                order_key = request.GET['key']
                participants = tour.participants.all().order_by(order_key)
                data = []
                for participant in participants:
                    participant_item = {}
                    for key, item in participant.__dict__.items():
                        if key != '_state':
                            participant_item[key] = item
                        if key == 'participant_id':
                            participant_data = Participant.objects.get(pk=key)
                            participant_item['name'] = participant_data['name']
                            participant_item['phone'] = participant_data['phone']
                    data.append(participant_item)

                return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)




