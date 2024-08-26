from django.views.generic import View, TemplateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...permissions import HasAdminAccessPermission



class AdminHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):
    template_name = 'dashboard/admin/home.html'
    
