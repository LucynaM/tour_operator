from django.shortcuts import render
from django.views import View
from .models import Offer
from .forms import AddOfferForm

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