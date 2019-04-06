from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import StaffForm

# Create your views here.

# staff admin management
class SuperUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class StaffListAdd(SuperUserPassesTestMixin, View):
    """Create, list staff"""

    def get(self, request):
        staff_list = User.objects.filter(is_staff=True).order_by('username')
        form = StaffForm()
        ctx = {
            'form': form,
            'staff_list': staff_list,
        }
        return render(request, 'webpage_staff/add_staff.html', ctx)

    def post(self, request):
        form = StaffForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('password2')
            form.cleaned_data['is_staff'] = True
            User.objects.create_user(**form.cleaned_data)
        staff_list = User.objects.filter(is_staff=True).order_by('username')
        ctx = {
            'form': form,
            'staff_list': staff_list,
        }
        return render(request, 'webpage_staff/add_staff.html', ctx)



class StaffEditDelete(SuperUserPassesTestMixin, View):

    def get(self, request, pk):
        staff = User.objects.get(pk=pk)
        form = StaffForm(instance=staff)
        ctx = {
            'form': form,
            'staff': staff
        }
        return render(request, 'webpage_staff/edit_staff.html', ctx)

    def post(self, request, pk):
        staff = User.objects.get(pk=pk)
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            if request.POST['submit'] == 'edytuj':
                staff.set_password(form.cleaned_data['password'])
                staff.save()
            elif request.POST['submit'] == 'usuń':
                staff.delete()
            return redirect('staff:add_staff')
        ctx = {
            'form': form,
        }
        return render(request, 'webpage_staff/edit_staff.html', ctx)
