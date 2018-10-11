from django.shortcuts import render, redirect
from django.views import View
from webpage_offer.models import Offer, Holiday, News

# Create your views here.

def search_snippet(request, page):
    try:
        search = request.POST['search']
        return redirect('webpage:search', search=search)
    except Exception as e:
        print(e)
        return render(request, page)

class HomePage(View):
    def get(self, request):
        return render(request, 'webpage/home.html')
    def post(self, request):
        try:
            search = request.POST['search']
            return redirect('webpage:search', search=search)
        except Exception as e:
            print(e)
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
    def post(self, request):
        search_snippet(request, 'webpage/home_for_school.html')


class HomeHolidayPage(View):
    def get(self, request):

        holiday = Holiday.objects.all()[0:1:-1]
        ctx = {
            'holiday': holiday,
        }
        return render(request, 'webpage/home_holiday.html', ctx)
    def post(self, request):
        search_snippet(request, 'webpage/home_holiday.html')


class HomeNewsPage(View):
    def get(self, request):

        news_list = News.objects.all().order_by('-pk')[0:2]
        ctx = {
            'news_list': news_list,
        }
        return render(request, 'webpage/home_news.html', ctx)
    def post(self, request):
        search_snippet(request, 'webpage/home_news.html')


class HomeSearchPage(View):
    def get(self, request, search):
        offer_list = Offer.objects.filter(direction__icontains=search)
        ctx = {
            'offer_list': offer_list,
        }
        return render(request, 'webpage/home_search.html', ctx)
    def post(self, request, search):
        search = request.POST['search']
        offer_list = Offer.objects.filter(direction__icontains=search)
        ctx = {
            'offer_list': offer_list,
        }
        return render(request, 'webpage/home_search.html', ctx)