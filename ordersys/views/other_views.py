from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login

from django.contrib.auth import views as auth_views
from django.utils.http import is_safe_url

from ..forms import *

class LogView(auth_views.LoginView):
    template_name = 'ordersys/other/login.html'
    model = LogInForm

    fields = ['username', 'password']
    def get(self, request):
        context = {
            'login_form': LogInForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        login_data = LogInForm(request.POST)
        if login_data.is_valid():    
            username = login_data.cleaned_data['username']
            password = login_data.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect = request.GET.get('next', '')
                if is_safe_url(url=redirect, allowed_hosts=settings.ALLOWED_HOSTS):
                    return HttpResponseRedirect(redirect)
                else:
                    return HttpResponseRedirect(reverse('ordersys:customers'))
            else:
                return HttpResponseRedirect(reverse('ordersys:login'))
