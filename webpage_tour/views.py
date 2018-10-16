from django.shortcuts import render
from django.views import View

from .models import Tour, TourParticipant, Participant
from .forms import TourForm, ParticipantForm

# Create your views here.


class AddTour(View):
    def get(self, request):
        form = TourForm()
        tour_list = Tour.objects.all()

        ctx = {
            'form': form,
            'tour_list': tour_list,
        }

        return render(request, 'webpage_tour/add_tour.html', ctx)


class EditTour(View):
    def get(self, request, pk):
        tour = Tour.objects.get(pk=pk)
        form = TourForm(instance=tour)
        ctx = {
            'tour': tour,
            'form': form,
        }
        return render(request, 'webpage_tour/edit_tour.html', ctx)