from django.shortcuts import render, redirect
from django.views import View

# Create your views here.

class HomePage(View):
    def get(self, request):
        return render(request, 'webpage/home.html')


class HomeForSchoolPage(View):
    def get(self, request):
        ctx = {}
        return render(request, 'webpage/home_for_school.html', ctx)
