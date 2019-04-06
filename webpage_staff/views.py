from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# Create your views here.

# staff admin management

class StaffListAdd(View):
    """Create, list staff"""

    def get(self, request):
        staff_list = User.objects.filter(is_staff=True).order_by('username')
        form = UserCreationForm()
        ctx = {
            'form': form,
            'staff_list': staff_list,
        }
        return render(request, 'webpage_staff/add_staff.html', ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)
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



class StaffEditDelete(View):

    def get(self, request, pk):
        staff = User.objects.get(pk=pk)
        form = UserChangeForm(instance=staff)
        ctx = {
            'form': form,
        }
        return render(request, 'webpage_staff/edit_staff.html', ctx)

    def post(self, request, pk):
        staff = User.objects.get(pk=pk)
        form = UserChangeForm(request.POST, instance=staff)
        if form.is_valid():
            if request.POST['submit'] == 'edit':
                form.save()
            elif request.POST['submit'] == 'delete':
                staff.delete()
            return redirect('staff:add_staff')
        ctx = {
            'form': form,
        }
        return render(request, 'webpage_staff/edit_staff.html', ctx)
