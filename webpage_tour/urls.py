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
from django.conf import settings
from django.conf.urls.static import static
from .views import AddTour, AddParticipant, EditTour, EditParticipant, ChangeStatus, generate_pdf, FillParticipant


urlpatterns = [
    url(r'^add_tour/$', AddTour.as_view(), name='add_tour'),
    url(r'^add_participant/(?P<pk>(\d)+)/$', AddParticipant.as_view(), name='add_participant'),
    url(r'^edit_tour/(?P<pk>(\d)+)/$', EditTour.as_view(), name='edit_tour'),
    url(r'^edit_participant/(?P<tour_pk>(\d)+)/(?P<participant_pk>(\d)+)/$', EditParticipant.as_view(), name='edit_participant'),
    url(r'^change_status/(?P<pk>(\d)+)/$', ChangeStatus.as_view(), name='change_status'),
    url(r'^generate_pdf/(?P<pk>(\d)+)/$', generate_pdf, name='generate_pdf'),
    url(r'^fill_participant/$', FillParticipant.as_view(), name='fill_participant'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
