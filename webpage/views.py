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


def getDirections():
    offer_list = Offer.objects.all()
    directions = []
    for offer in offer_list:
        for direction in offer.direction.split(', '):
            if direction not in directions:
                directions.append(direction)
    directions = ', '.join(directions)
    return directions


class HomePage(View):
    def get(self, request):
        directions = getDirections()
        ctx = {
            'directions': directions,
        }
        return render(request, 'webpage/home.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home.html')




class HomeForSchoolPage(View):
    def get(self, request):
        for_school = Offer.objects.filter(category='school_trip', selected=False).exclude(withdrawn=True).order_by('title')
        for_school_selected = Offer.objects.filter(category='school_trip', selected=True).order_by('selected_sort')
        directions = getDirections()
        ctx = {
            'for_school': for_school,
            'for_school_selected': for_school_selected,
            'directions': directions,
        }
        return render(request, 'webpage/home_for_school.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_for_school.html')


class HomePilgrimagePage(View):
    def get(self, request):
        pilgrimage = Offer.objects.filter(category='pilgrimage', selected=False).exclude(withdrawn=True).order_by('title')
        pilgrimage_selected = Offer.objects.filter(category='pilgrimage', selected=True).order_by('selected_sort')
        directions = getDirections()
        ctx = {
            'pilgrimage': pilgrimage,
            'pilgrimage_selected': pilgrimage_selected,
            'directions': directions,
        }
        return render(request, 'webpage/home_pilgrimage.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_pilgrimage.html')
    
    
class HomeForWorkPage(View):
    def get(self, request):
        for_work = Offer.objects.filter(category='work_trip', selected=False).exclude(withdrawn=True).order_by('title')
        for_work_selected = Offer.objects.filter(category='work_trip', selected=True).order_by('selected_sort')
        directions = getDirections()
        ctx = {
            'for_work': for_work,
            'for_work_selected': for_work_selected,
            'directions': directions,
        }
        return render(request, 'webpage/home_for_work.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_for_work.html')


class HomeRecommendedPage(View):
    def get(self, request):
        recommended = Offer.objects.filter(recommended=True).order_by('recommended_sort')
        directions = getDirections()
        ctx = {
            'recommended': recommended,
            'directions': directions,
        }
        return render(request, 'webpage/home_recommended.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_recommended.html')


class HomeHolidayPage(View):
    def get(self, request):
        holiday = Holiday.objects.all()[0:1:-1]
        directions = getDirections()
        ctx = {
            'holiday': holiday,
            'directions': directions,
        }
        return render(request, 'webpage/home_holiday.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_holiday.html')


class HomeNewsPage(View):
    def get(self, request):
        news_list = News.objects.all().order_by('-pk')[0:2]
        directions = getDirections()
        ctx = {
            'news_list': news_list,
            'directions': directions,
        }
        return render(request, 'webpage/home_news.html', ctx)
    def post(self, request):
        return search_snippet(request, 'webpage/home_news.html')


class HomeSearchPage(View):
    def get(self, request, search):
        offer_list = Offer.objects.filter(direction__icontains=search)
        directions = getDirections()
        ctx = {
            'offer_list': offer_list,
            'directions': directions,
        }
        return render(request, 'webpage/home_search.html', ctx)
    def post(self, request, search):
        search = request.POST['search']
        offer_list = Offer.objects.filter(direction__icontains=search)
        directions = getDirections()
        ctx = {
            'offer_list': offer_list,
            'directions': directions,
        }
        return render(request, 'webpage/home_search.html', ctx)