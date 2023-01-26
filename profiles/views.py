

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect

from chatterbox.models import Room, Message
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.shortcuts import render

from profiles.models import Profile


# Create your views here.

@login_required
def profiles_list(request):
    profiles =Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "profiles/users.html", context)

@login_required
def user_profile(request, pk):
    #user = User.objects.get(id=pk)
    profile = Profile.objects.get(id=pk) # Profile beru z models.py
    context = {"profile":profile}
    return render(request, "profiles/user.html", context)

class ProfileEditFrom(ModelForm):
    class Meta:
        model = Profile
        fields = ("about_me", "photo")

class EditProfile(UpdateView):
    template_name = "profiles/edit_user.html"
    model = Profile
    form_class = ProfileEditFrom
    success_url = reverse_lazy("profiles")