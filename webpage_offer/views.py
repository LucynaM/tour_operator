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


class SelectOffer(View):
    def get(self, request):
        school_offer = Offer.objects.filter(category__icontains='school').exclude(selected=True)
        school_selected = Offer.objects.filter(selected=True).order_by("selected_sort")
        ctx = {
            'school_offer': school_offer,
            'school_selected': school_selected,
        }
        return render(request, 'webpage_offer/select_school.html', ctx)


class SetSelected(View):
    def get(self, request):
        try:
            if 'old_id' in request.GET.keys():
                old_id = int(request.GET['old_id'])
                old_selected = Offer.objects.get(pk=old_id)
                old_selected.selected = False
                old_selected.selected_sort = None
                old_selected.save()

            new_id = int(request.GET['new_id'])
            sort = int(request.GET['sort'])
            new_selected = Offer.objects.get(pk=new_id)
            new_selected.selected = True
            new_selected.selected_sort = sort
            new_selected.save()
            data = {
                "ok": "ok",
            }
            return JsonResponse(data)
        except Exception as e:
            print(e)
