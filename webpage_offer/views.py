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
            form = AddOfferForm()
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
        all_offer = Offer.objects.all().order_by('category', 'title')
        categories = ['pilgrimage', 'school_trip', 'work_trip']

        ctx = {
            'all_offer': all_offer,
            'categories': categories,
        }
        return render(request, 'webpage_offer/select_offer.html', ctx)


def process_offer(request, func1, func2):
    if 'old_id' in request.GET.keys():
        old_id = int(request.GET['old_id'])
        old_element = Offer.objects.get(pk=old_id)
        func1(old_element)

    new_id = int(request.GET['new_id'])
    sort = int(request.GET['sort'])
    new_element = Offer.objects.get(pk=new_id)
    offer = func2(new_element, sort)
    data = []

    for item in offer:
        data_element = {}
        for attr, value in item.__dict__.items():
            if attr in ['id', 'title', 'duration_in_days', 'category']:
                data_element[attr] = value
        data.append(data_element)

    return data


class SetSelected(View):
    def old_element_deselect(self, obj):
        obj.selected = False
        obj.selected_sort = None
        obj.save()

    def new_element_select(self, obj, sort):
        obj.selected = True
        obj.selected_sort = sort
        obj.save()
        return Offer.objects.filter(category=obj.category, selected=False).order_by('title')

    def get(self, request):
        try:
            data = process_offer(request, self.old_element_deselect, self.new_element_select)
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)


class SetRecommended(View):
    def old_element_unrecommend(self, obj):
        obj.recommended = False
        obj.recommended_sort = None
        obj.save()

    def new_element_recommend(self, obj, sort):
        obj.recommended = True
        obj.recommended_sort = sort
        obj.save()
        return Offer.objects.filter(recommended=False).order_by('category', 'title')

    def get(self, request):
        try:
            data = process_offer(request, self.old_element_unrecommend, self.new_element_recommend)
            data.append('recommendation')
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)
