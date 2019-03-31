from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from webpage_offer.models import Offer, News
from datetime import datetime
from webpage_tour.views import get_dates

# Create your views here.


def search_snippet(request, page):
    try:
        search = request.POST['search']
        if " " in search:
            search = search.replace(' ', '_')
        if ". " in search:
            search = search.replace('. ', ' ')

        return redirect('webpage:search', search=search)
    except Exception as e:
        print(e)
        return render(request, page)


class HomePage(View):
    def get(self, request):
        return render(request, 'webpage/home.html')
    def post(self, request):
        return search_snippet(request, 'webpage/home.html')


class OfferPage(View):
    def get(self, request):
        category = request.path[1:-1]
        offer = Offer.objects.filter(category=category, selected=False).exclude(category="holiday", withdrawn=True).order_by('title')
        offer_chunk = ((offer[x:x+2]) for x in range(0, len(offer), 2))
        offer_selected = Offer.objects.filter(category=category, selected=True).order_by('selected_sort')
        ctx = {
            'category': category,
            'offer_all': offer_chunk,
            'offer_selected': offer_selected,
        }
        return render(request, 'webpage/home_offer.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_offer.html')


class HomeRecommendedPage(View):
    def get(self, request):
        recommended = Offer.objects.filter(recommended=True).order_by('recommended_sort')

        ctx = {
            'recommended': recommended,
        }
        return render(request, 'webpage/home_recommended.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_recommended.html')


class HomeHolidayPage(View):
    def get(self, request):
        holiday = Offer.objects.filter(category="holiday").exclude(withdrawn=True).order_by('-tours__open', 'title')
        for item in holiday:
            item.holiday_tours = []
            for tour in item.tours.all().exclude(end_date__lte=datetime.now().date()).order_by('start_date'):
                holiday_tour = {}
                tour.date = get_dates(tour.start_date, tour.end_date)
                holiday_tour["dates"] = tour.date
                holiday_tour["open"] = tour.open
                item.holiday_tours.append(holiday_tour)
        ctx = {
            'offer_all': holiday,
        }

        return render(request, 'webpage/home_holiday.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_holiday.html')


class HomeNewsPage(View):
    def get(self, request):
        news_list = News.objects.all().order_by('-pk')
        news_list_chunk = ((news_list[x:x+2]) for x in range(0, len(news_list), 2))

        # present split result list in pages
        paginator = Paginator(news_list, 2)


        page = request.GET.get('page', 1)
        try:
            news_result = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            news_result = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            news_result = paginator.page(paginator.num_pages)
        ctx = {
            'news_list': news_list_chunk,
            'news_result': news_result,
        }
        return render(request, 'webpage/home_news.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_news.html')


class HomeSearchPage(View):
    def get(self, request, search):
        if '_' in search:
            search = search.replace('_', ' ')
        if ". " in search:
            search = search.replace('. ', ' ')
        offer = Offer.objects.filter(direction__icontains=search)
        offer_chunk = ((offer[x:x + 2]) for x in range(0, len(offer), 2))

        ctx = {
            'offer_all': offer_chunk,
            'category': search,

        }
        return render(request, 'webpage/home_search.html', ctx)
    def post(self, request, search):
        search = request.POST['search']
        if '_' in search:
            search = search.replace('_', ' ')
        if ". " in search:
            search = search.replace('. ', ' ')
        offer = Offer.objects.filter(direction__icontains=search)
        offer_chunk = ((offer[x:x + 2]) for x in range(0, len(offer), 2))

        ctx = {
            'offer_all': offer_chunk,
            'category': search,
        }

        return render(request, 'webpage/home_search.html', ctx)


class GetDirectionsBis(View):
    def get(self, request):
        try:
            offer_list = Offer.objects.exclude(withdrawn=True)
            data = {}
            data['directions'] = []
            for offer in offer_list:
                for direction in offer.direction.split('; '):
                    if direction not in data['directions']:
                        data['directions'].append(direction)
            return JsonResponse(data)
        except Exception as e:
            print(e)