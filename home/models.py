from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _ #翻訳
import uuid as uuid_lib

GENDER_CHOICES = (
    ('man', 'man'),
    ('woman', 'woman'),
)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email mast be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(emai, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid_lib.uuid4,primary_key=True, editable=False)

    email = models.EmailField(_('email address'), unique=True)
    nick_name = models.CharField(_('ニックネーム'), max_length=150, blank=True)

    birthday = models.DateField(_('birthday'), null=True)
    gender = models.CharField(_('gender'), max_length=6, choices=GENDER_CHOICES, null=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default = False,
        help_text =_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default = True,
        help_text =_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    #def get_full_name(self):
    #    full_name = '%s' % (self.nick_name)
    #    return full_name.strip()
    
    #def get_short_name(self):
    #    return self.nick_name
    
    #def email_user(self, subject, message, from_email=None, **kwargs):
    #    send_mail(subject, message, from_email, [self.email], **kwargs)