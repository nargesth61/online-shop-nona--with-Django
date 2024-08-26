from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import UserType


class DashboardHomeView(LoginRequiredMixin,View):
    """
     View class that redirects authenticated users to their respective dashboards 
     based on user type, and redirects unauthenticated users to the login page.
    """
    def dispatch(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.type == UserType.customer.value:
                return redirect(reverse_lazy('dashboard:customer:home'))
            if request.user.type == UserType.admin.value:
                return redirect(reverse_lazy('dashboard:admin:home'))
        else:
            return redirect(reverse_lazy('accounts:login'))
        return super().dispatch(request, *args, **kwargs)
    