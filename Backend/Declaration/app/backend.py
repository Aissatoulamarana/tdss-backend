from django.contrib.auth.backends import ModelBackend
from app.models import CustomUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)

            # Vérification du statut utilisateur
            if hasattr(user, "status") and user.status != 'actif':
                return None  # Refuser la connexion pour un utilisateur inactif

            # Vérification pour les comptes bancaires
            if hasattr(user, "is_active") and not user.is_active:
                return None  # Refuser la connexion pour un compte bancaire inactif

            # Vérifier le mot de passe
            if user.check_password(password):
                return user
            else:
                return None

        except CustomUser.DoesNotExist:
            return None
