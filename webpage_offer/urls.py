"""tour_operator_mp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import AddListOffer, EditOffer, ShowOffer, SelectOffer, SetSelected, SetRecommended, \
    AddListHoliday, EditHoliday, ShowHoliday, AddListNews, EditNews, ShowNews, TourManager

urlpatterns = [
    url(r'^manager/$', TourManager.as_view(), name='tour_manager'),

    url(r'^add_offer/$', AddListOffer.as_view(), name='add_offer'),
    url(r'^edit_offer/(?P<pk>[0-9]+)/$', EditOffer.as_view(), name='edit_offer'),
    url(r'^show_offer/(?P<pk>[0-9]+)/$', ShowOffer.as_view(), name='show_offer'),

    url(r'^select_offer/$', SelectOffer.as_view(), name='select_offer'),
    url(r'^set_selected/$', SetSelected.as_view(), name='set_selected'),
    url(r'^set_recommended/$', SetRecommended.as_view(), name='set_recommended'),

    url(r'^add_holiday/$', AddListHoliday.as_view(), name='add_holiday'),
    url(r'^edit_holiday/(?P<pk>[0-9]+)/$', EditHoliday.as_view(), name='edit_holiday'),
    url(r'^show_holiday/(?P<pk>[0-9]+)/$', ShowHoliday.as_view(), name='show_holiday'),

    url(r'^add_news/$', AddListNews.as_view(), name='add_news'),
    url(r'^edit_news/(?P<pk>(\d)+)/$', EditNews.as_view(), name='edit_news'),
    url(r'^show_news/(?P<pk>(\d)+)/$', ShowNews.as_view(), name='show_news'),
]
