from django.shortcuts import render, redirect
from django.views import View

# Create your views here.

class HomePage(View):
    def get(self, request):
        return render(request, 'tour_operator_app/home.html')


class HomeForSchoolPage(View):
    def get(self, request):
        ctx = {}
        return render(request, 'tour_operator_app/home_for_school.html', ctx)