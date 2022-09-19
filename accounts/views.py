from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.urls import reverse_lazy
from django.views import generic

# tady je změna - dělám view pomocí třídy - další možnost je pomocí funkce


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (#"first_name", "last_name",
                  "username","email" ,"password1", "password2")


class SignUpView(generic.CreateView):
    form_class = SignUpForm #UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'accounts/signup.html'
