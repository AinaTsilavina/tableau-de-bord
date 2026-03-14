from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
class UserManager(BaseUserManager):
     #Manager personnalisé pour le modèle Utilisateur.
     def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Le champ 'username' est obligatoire.")
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

     def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    #Modèle utilisateur personnalisé

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nom d'utilisateur"
    )

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Membre du staff")
    is_members = models.BooleanField(
        _("members status"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as members. "
           
        ),
    )
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username
