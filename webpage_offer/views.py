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
        all_offer = Offer.objects.filter(recommended=False).order_by('category', 'title')
        all_offer_recommended = Offer.objects.filter(recommended=True).order_by('recommended_sort')
        school_offer = Offer.objects.filter(category='school_trip', selected=False).order_by('title')
        school_selected = Offer.objects.filter(category='school_trip', selected=True).order_by('selected_sort')
        pilgrimage_offer = Offer.objects.filter(category='pilgrimage', selected=False).order_by('title')
        pilgrimage_selected = Offer.objects.filter(category='pilgrimage', selected=True).order_by('selected_sort')
        work_offer = Offer.objects.filter(category='work_trip', selected=False).order_by('title')
        work_selected = Offer.objects.filter(category='work_trip', selected=True).order_by('selected_sort')

        ctx = {
            'all_offer': all_offer,
            'all_offer_recommended': all_offer_recommended,
            'school_offer': school_offer,
            'school_selected': school_selected,
            'pilgrimage_offer': pilgrimage_offer,
            'pilgrimage_selected': pilgrimage_selected,
            'work_offer': work_offer,
            'work_selected': work_selected,
        }
        return render(request, 'webpage_offer/select_offer.html', ctx)


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
            offer = Offer.objects.filter(category=new_selected.category, selected=False).order_by('title')
            data = []

            for item in offer:
                data_element = {}
                for attr, value in item.__dict__.items():
                    if attr in ['id', 'title', 'duration_in_days', 'category']:
                        data_element[attr] = value
                data.append(data_element)

            return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)


class SetRecommended(View):

    def get(self, request):
        try:
            if 'old_id' in request.GET.keys():
                old_id = int(request.GET['old_id'])
                old_recommended = Offer.objects.get(pk=old_id)
                old_recommended.recommended = False
                old_recommended.recommended_sort = None
                old_recommended.save()

            new_id = int(request.GET['new_id'])
            sort = int(request.GET['sort'])
            new_recommended = Offer.objects.get(pk=new_id)
            new_recommended.recommended = True
            new_recommended.recommended_sort = sort
            new_recommended.save()
            offer = Offer.objects.filter(recommended=False).order_by('category', 'title')
            data = []

            for item in offer:
                data_element = {}
                for attr, value in item.__dict__.items():
                    if attr in ['id', 'title', 'duration_in_days', 'category']:
                        data_element[attr] = value
                data.append(data_element)
            data.append('recommendation')

            return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)