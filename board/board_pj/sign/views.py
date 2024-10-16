from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'