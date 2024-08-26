from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from accounts.forms import AuthenticationForm,RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login,authenticate
from .models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.tokens import generate_verification_token
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings



def register(request):
    """
    View for user registration with email verification.
    Displays the registration form and handles form submission.
    Sends a verification email to the user's email address.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)   
        if form.is_valid():      
            user = form.save(commit=False)
            user.is_active = False
            user.is_verified = False
            user.created_date = datetime.now()
            user.last_login = datetime.now()
            user.save()

            # Send verification email
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_verification_token.make_token(user),
                })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
        
            return render(request, 'accounts/registration_complete.html')

    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def verify_email(request, uidb64, token):
    """
    View for email verification.
    Verifies the email verification token and updates the user's status to active if valid.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        return render(request, 'accounts/verification_invalid.html')
    if user is not None and  generate_verification_token.check_token(user,token):
                user.is_active = True
                user.is_verified = True
                user.save()
                login(request, user)  # Automatically logs in the user after verification
                return render(request, 'accounts/email_verified.html')
    else:
            return render(request, 'accounts/verification_invalid.html')


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = form.get_user()

        if user is not None and not user.is_verified:
            messages.error(self.request, "Your account is not verified. Please check your email.")
            return HttpResponseRedirect(reverse_lazy('login'))

        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle invalid login attempts
        return super().form_invalid(form)

class LogoutView(auth_views.LogoutView):
    pass