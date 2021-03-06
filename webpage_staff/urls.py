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
from django.contrib.auth import views as auth_views
from .views import StaffListAdd, StaffEdit, DeleteItem


urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'webpage_staff/login.html'},  name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'staff:login'}, name='logout'),
    url(r'^add_staff/$', StaffListAdd.as_view(), name='add_staff'),
    url(r'^edit_staff/(?P<pk>[0-9]+)/$', StaffEdit.as_view(), name='edit_staff'),
    url(r'^delete_item/(?P<pk>[0-9]+)/$', DeleteItem.as_view(), name='delete_item'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
