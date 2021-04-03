from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, name, email, phone_number, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(name=name, phone_number=phone_number,email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, name, email=None, **extra_fields):
        return self._create_user(name, email, phone_number, password, False, False, **extra_fields)

    def create_superuser(self, name, email, phone_number, **extra_fields):
        user=self._create_user(email, name, phone_number, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=15, help_text=('Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters'))
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    is_staff = models.BooleanField(default=False, help_text=('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=True, help_text=('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

class UserToken(models.Model):
    user = models.ForeignKey(User, models.PROTECT, related_name='token')
    token = models.CharField(max_length=255, unique=True, null=False, blank=False)

class Score(models.Model):
    user = models.ForeignKey(User, models.PROTECT, related_name='score')
    score = models.IntegerField(null=False, blank=False)