from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Offer
from .forms import AddOfferForm, EditOfferForm

# Create your views here.

class AddListOffer(View):
    """Show all offer and add new one"""

    def get(self, request):
        offer_list = Offer.objects.all().order_by('category', 'title')
        form = AddOfferForm()
        ctx = {
            'offer_list': offer_list,
            'form': form,
               }
        return render(request, 'webpage_offer/add_offer.html', ctx)

    def post(self, request):
        form = AddOfferForm(request.POST, request.FILES)
        if form.is_valid():
            Offer.objects.create(**form.cleaned_data)
        offer_list = Offer.objects.all().order_by('category', 'title')
        ctx = {
            'offer_list': offer_list,
            'form': form,
        }
        return render(request, 'webpage_offer/add_offer.html', ctx)


class EditOffer(View):

    def get(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        form = EditOfferForm(instance=offer)
        ctx = {
            'form': form,
            'offer': offer,
        }
        return render(request, 'webpage_offer/edit_offer.html', ctx)

    def post(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        form = EditOfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
        offer = Offer.objects.get(pk=pk)
        ctx = {
            'form': form,
            'offer': offer,
        }
        return render(request, 'webpage_offer/edit_offer.html', ctx)



class ShowOffer(View):

    def get(self, request, pk):
        try:
            offer = Offer.objects.get(pk=pk)
            data = {}
            for attr, value in offer.__dict__.items():
                if attr != '_state':
                    data[attr] = value
            # print(data)
            return JsonResponse(data)
        except Exception as e:
            print(e)
