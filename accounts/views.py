from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# tady je změna - ělám view pomocí třídy - další možnost je pomocí funkce
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'accounts/signup.html'
