import sys, os
from django import forms
from .models import Artist, Live, Audience
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
sys.path.append('../')
from home.models import User

class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = ('name','url','Twitter',)


class LiveForm(forms.ModelForm):

    class Meta:
        model = Live
        fields = ('name', 'artists', 'place', 'url', 'date', 'open_time', 'start_time', 'adv', 'door', 'published_date',)

class AudienceForm(forms.ModelForm):

    class Meta:
        model = Audience
        fields = ('live', 'name', 'ticket',)

class AudienceDetailForm(forms.ModelForm):
    
    class Meta:
        model = Audience
        fields = ('name', 'ticket',)

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'メールアドレス'

        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'
    
class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    nick_name = forms.CharField(required=True)
    birthday = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'nick_name','birthday','gender',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nick_name'].widget.attrs['class'] = 'form-control'
        self.fields['nick_name'].widget.attrs['placeholder'] = 'お名前'
 
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'OOOO@OO.OO'

        self.fields['birthday'].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['placeholder'] = 'OOOO-OO-OO'

        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['gender'].widget.attrs['placeholder'] = '性別'
 
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
  
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'

class UserPasswordChangeForm(PasswordChangeForm):
    pass