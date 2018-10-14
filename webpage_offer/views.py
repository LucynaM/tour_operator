from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Offer, Holiday, News
from .forms import AddOfferForm, EditOfferForm, HolidayForm, NewsForm

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
        form = AddOfferForm(request.POST)
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


def show_elements(obj):
    data = {}
    for attr, value in obj.__dict__.items():
        if attr != '_state':
            data[attr] = value
    return data


class ShowOffer(View):

    def get(self, request, pk):
        try:
            offer = Offer.objects.get(pk=pk)
            data = show_elements(offer)

            return JsonResponse(data)
        except Exception as e:
            print(e)


class ShowHoliday(View):

    def get(self, request, pk):
        try:
            holiday = Holiday.objects.get(pk=pk)
            data = show_elements(holiday)

            return JsonResponse(data)
        except Exception as e:
            print(e)


class ShowNews(View):

    def get(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
            data = show_elements(news)

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


def process_offer(request, func1, func2, get_result):
    if 'old_id' in request.GET.keys():
        old_id = int(request.GET['old_id'])
        old_element = Offer.objects.get(pk=old_id)
        func1(old_element)

    if 'new_id' in request.GET.keys():
        new_id = int(request.GET['new_id'])
        sort = int(request.GET['sort'])
        new_element = Offer.objects.get(pk=new_id)
        func2(new_element, sort)
        offer = get_result(new_element)
    else:
        offer = get_result(old_element)

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

    def get_result(self, obj):
        return Offer.objects.filter(category=obj.category, selected=False).order_by('title')

    def get(self, request):
        try:
            data = process_offer(request, self.old_element_deselect, self.new_element_select, self.get_result)
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

    def get_result(self, obj):
        return Offer.objects.filter(recommended=False).order_by('category', 'title')

    def get(self, request):
        try:
            data = process_offer(request, self.old_element_unrecommend, self.new_element_recommend, self.get_result)
            data.append('recommendation')
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)


class AddListHoliday(View):
    def get(self, request):
        holiday_list = Holiday.objects.all().order_by('-pk')
        form = HolidayForm()
        ctx = {
            'holiday_list': holiday_list,
            'form': form,
        }
        return render(request, 'webpage_offer/add_holiday.html', ctx)

    def post(self, request):
        form = HolidayForm(request.POST)

        if form.is_valid():
            holiday = form.save()
            return redirect('offer:edit_holiday', pk=holiday.pk)
        ctx = {
            'form': form,
        }
        return render(request, 'webpage_offer/add_holiday.html', ctx)


class EditHoliday(View):
    def get(self, request, pk):
        holiday = Holiday.objects.get(pk=pk)
        form = HolidayForm(instance=holiday)
        ctx = {
            'form': form,
            'holiday': holiday,

        }
        return render(request, 'webpage_offer/edit_holiday.html', ctx)

    def post(self, request, pk):
        holiday = Holiday.objects.get(pk=pk)
        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            form.save()
        holiday = Holiday.objects.get(pk=pk)
        ctx = {
            'form': form,
            'holiday': holiday,
        }
        return render(request, 'webpage_offer/edit_holiday.html', ctx)


class AddListNews(View):
    def get(self, request):
        news_list = News.objects.all().order_by('entry_date')
        form = NewsForm()
        ctx = {
            'news_list': news_list,
            'form': form,
        }
        return render(request, 'webpage_offer/add_news.html', ctx)

    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            form = NewsForm()
        news_list = News.objects.all().order_by('entry_date')
        ctx = {
            'news_list': news_list,
            'form': form,
        }
        return render(request, 'webpage_offer/add_news.html', ctx)


class EditNews(View):
    def get(self, request, pk):
        news = News.objects.get(pk=pk)
        form = NewsForm(instance=news)

        ctx = {
            'form': form,
            'news': news,
        }
        return render(request, 'webpage_offer/edit_news.html', ctx)

    def post(self, request, pk):
        news = News.objects.get(pk=pk)
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            news = form.save()
        ctx = {
            'form': form,
            'news': news,
        }
        return render(request, 'webpage_offer/edit_news.html', ctx)
