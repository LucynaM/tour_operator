from django.shortcuts import render, redirect
from django.views import View
from webpage_offer.models import Offer, Holiday, News

# Create your views here.

class HomePage(View):
    def get(self, request):
        return render(request, 'webpage/home.html')


class HomeForSchoolPage(View):
    def get(self, request):
        for_school = Offer.objects.filter(category='school_trip', selected=False).order_by('title')
        for_school_selected = Offer.objects.filter(category='school_trip', selected=True).order_by('selected_sort')
        ctx = {
            'for_school': for_school,
            'for_school_selected': for_school_selected,
        }
        return render(request, 'webpage/home_for_school.html', ctx)


class HomeHolidayPage(View):
    def get(self, request):

        holiday = Holiday.objects.all()[0:1:-1]
        ctx = {
            'holiday': holiday,
        }
        return render(request, 'webpage/home_holiday.html', ctx)

class HomeNewsPage(View):
    def get(self, request):

        news_list = News.objects.all().order_by('-pk')[0:2]
        ctx = {
            'news_list': news_list,
        }
        return render(request, 'webpage/home_news.html', ctx)
