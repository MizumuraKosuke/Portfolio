import sys, os
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArtistForm, LiveForm, AudienceForm,  AudienceDetailForm, LoginForm, RegisterForm, UserPasswordChangeForm
from .models import Activate, Live, Artist

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views import generic
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token_manager import create_expiration_date, create_key

sys.path.append('../')
from port import settings

User = get_user_model()

@login_required
def profile(request):
    context = {
        'users': request.user,
    }
    return render(request, 'reserve/profile.html', context)

def login(request):
    context = {
        'template_name': 'reserve/login.html',
        'authentication_form': LoginForm,
    }
    return auth_views.login(request, **context)

def logout(request):
    context = {
        'template_name': 'reserve/reserve.html',
    }
    return auth_views.logout(request, **context)

class CreateUserView(generic.CreateView):
    template_name = 'reserve/create.html'
    form_class = RegisterForm
    success_url = reverse_lazy('create_done')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active= False
        user.save()
        activate_key = create_key()
        expiration_date = create_expiration_date()
        activate_instance = Activate(user=user, key=activate_key, expiration_date=expiration_date)
        activate_instance.save()
        current_site = get_current_site(self.request)
        domain = current_site.domain
        message_template = get_template('mailtemplate/new/create_user.txt')
        uid = force_text(urlsafe_base64_encode(force_bytes(activate_key)))

        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'uid': uid,
            'user': user,
        }

        subject = "ご登録ありがとうございます"
        message = message_template.render(context)
        from_email = settings.EMAIL_HOST_USER
        to = [user.email]
        send_mail(subject, message, from_email, to)

        result = super().form_valid(form)

        messages.success(
            self.request, '{}様宛に会員登録用のURLを記載したメールを送信しました。'.format(user.nick_name)
        )
        return result

class CreateDoneView(generic.TemplateView):
    template_name = 'reserve/create_done.html'

class CreateCompleteView(generic.TemplateView):
    template_name = 'reserve/create_complete.html'

    def get(self, request, **kwargs):
        uidb64 = kwargs.get("uidb64")

        try:
            key = force_text(urlsafe_base64_decode(uidb64))
            activate = get_object_or_404(Activate, key=key)
            user = activate.user
            expiration_date = activate.expiration_date
            t_now = datetime.now()
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user and not user.is_active and t_now <= expiration_date:
            context = super(CreateCompleteView, self).get_context_data(**kwargs)

            user.is_active = True
            user.save()
            user.backend = 'user.backends.EmailModelBackend'
            auth_login(request, user)
            responce_message = "本登録が完了しました"
            context['message'] = responce_message
            Activate.objects.filter(key=key).delete()
            return render(self.request, self.template_name, context)
        else:
            Activate.objects.filter(key=key).delete()
            if user :
                User.objects.filter(uuid=User.uuid).delete()
            return render(request, 'reserve/create_failed.html')

def reserve(request):
    return render(request, 'reserve/reserve.html', {})

def audience(request):
    lives = None
    if request.method == "GET":
        if "serch_artist" in request.GET:
            artist_value = request.GET.get("artists")
            lives = Live.objects.filter(artists__name=artist_value)
        elif "serch_place" in request.GET:
            place_value = request.GET.get("place")
            lives = Live.objects.filter(place__icontains=place_value)
        elif "serch_name" in request.GET:
            name_value = request.GET.get("name")
            lives = Live.objects.filter(name__icontains=name_value)
    form = LiveForm()
    return render(request, 'reserve/audience.html', {'form': form, 'lives': lives})

def live_detail(request, pk):
    live = get_object_or_404(Live, pk=pk)
    return render(request, 'reserve/live_detail.html', {'live': live})

@login_required
def live_reserve(request, pk):
    live = get_object_or_404(Live, pk=pk)
    if request.method == "POST":
        form = AudienceDetailForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.live = live
            post.user = request.user
            post.save()

            reserve_user = post.user
            from_email = settings.EMAIL_HOST_USER
            subject_user = "チケットの取り置きが完了しました。"
            message_template_user = get_template('mailtemplate/new/reserve_user.txt')
            message_user = message_template_user.render({'reserve_user': reserve_user, 'audience': post})
            to_user = [reserve_user.email]
            send_mail(subject_user, message_user, from_email, to_user)
            messages.success(
                request, '{}様宛に確認メールを送信しました。'.format(reserve_user.nick_name)
                )

            org = live.user
            subject_org = "チケットの予約が入りました。"
            message_template_org = get_template('mailtemplate/new/reserve_organizer.txt')
            message_org = message_template_org.render({'org': org, 'audience': post})
            to_org = [org.email]
            send_mail(subject_org, message_org, from_email, to_org)
            messages.success(
                request, '{}様宛に確認メールを送信しました。'.format(org.nick_name)
                )
                
            return render(request, 'reserve/reserve_success.html', {'reserve_user': reserve_user, 'live': live})
    else:
        form = AudienceForm()
    return render(request, 'reserve/live_reserve.html', {'form': form, 'live': live})

@login_required
def reserve_form(request):
    if request.method == "POST":
        form = AudienceForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            live = post.live

            reserve_user = post.user
            from_email = settings.EMAIL_HOST_USER
            subject_user = "チケットの取り置きが完了しました。"
            message_template_user = get_template('mailtemplate/new/reserve_user.txt')
            message_user = message_template_user.render({'reserve_user': reserve_user, 'audience': post})
            to_user = [reserve_user.email]
            send_mail(subject_user, message_user, from_email, to_user)
            messages.success(
                request, '{}様宛に確認メールを送信しました。'.format(reserve_user.nick_name)
                )

            org = live.user
            subject_org = "チケットの予約が入りました。"
            message_template_org = get_template('mailtemplate/new/reserve_organizer.txt')
            message_org = message_template_org.render({'org': org, 'audience': post})
            to_org = [org.email]
            send_mail(subject_org, message_org, from_email, to_org)
            messages.success(
                request, '{}様宛に確認メールを送信しました。'.format(org.nick_name)
                )

            return render(request, 'reserve/reserve_success.html', {'reserve_user': reserve_user, 'live': live})
    else:
        form = AudienceForm()
    return render(request, 'reserve/reserve_form.html', {'form': form})

@login_required
def create_live(request):
    if request.method == "POST":
        form = LiveForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            return render(request, 'reserve/reserve.html', {})
    else:
        form = LiveForm()
    return render(request, 'reserve/create_live.html', {'form': form})

def create_artist(request):
    if request.method == "POST":
        form = ArtistForm(request.POST)
        if form.is_valid():
            post = form.save()
            return render(request, 'reserve/reserve.html', {})
    else:
        form = ArtistForm()
    return render(request, 'reserve/create_artist.html', {'form': form})
