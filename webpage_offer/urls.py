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
from .views import AddListOffer, EditOffer, ShowOffer, SelectOffer, SetSelected

urlpatterns = [
    url(r'^add/$', AddListOffer.as_view(), name='add_offer'),
    url(r'^edit/(?P<pk>[0-9]+)/$', EditOffer.as_view(), name='edit_offer'),
    url(r'^show/(?P<pk>[0-9]+)/$', ShowOffer.as_view(), name='show_offer'),
    url(r'^select/$', SelectOffer.as_view(), name='select_offer'),
    url(r'^set_selected/$', SetSelected.as_view(), name='set_selected'),
]
