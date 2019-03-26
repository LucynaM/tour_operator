from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from webpage_offer.models import Offer, Holiday, News

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
        offer = Offer.objects.filter(category=category, selected=False).exclude(withdrawn=True).order_by('title')
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
        holiday = Holiday.objects.all().exclude(withdrawn=True)

        ctx = {
            'offer_all': holiday,
        }
        return render(request, 'webpage/home_holiday.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_holiday.html')


class HomeNewsPage(View):
    def get(self, request):
        news_list = News.objects.all().order_by('-pk')[0:2]

        ctx = {
            'news_list': news_list,
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
        offer_len = len(offer) % 2 == 0

        holiday = Holiday.objects.filter(direction__icontains=search)
        holiday_chunk = ((holiday[x:x + 2]) for x in range(0, len(holiday), 2))

        ctx = {
            'offer_all': offer_chunk,
            'holiday_all': holiday_chunk,
            'offer_len': offer_len,
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