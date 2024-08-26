from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import User

class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)
        
        if not user.is_active:
            raise ValidationError("user is not verified")
     
       

class RegistrationForm(UserCreationForm):
    """
      Registration form for creating new users with email verification.
    """
    class Meta:
        model = User
        fields = ( 'email','password1', 'password2')