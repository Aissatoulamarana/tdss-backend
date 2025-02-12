from django.contrib.auth.backends import ModelBackend
from app.models import CustomUser
from django.core.exceptions import PermissionDenied

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Vérification de l'existence de l'utilisateur par email
            user = CustomUser.objects.get(email=username)

            # Vérification du statut avant l'authentification
            if user.status != 'actif':
                # Si l'utilisateur n'est pas actif, on lève une exception
                raise PermissionDenied(f"Votre compte est {user.status}. Il doit être activé.")

            # Authentification avec le mot de passe
            if user.check_password(password):
                return user
            else:
                return None

        except CustomUser.DoesNotExist:
            # Si l'utilisateur n'existe pas, renvoyer None
            return None
        except PermissionDenied as e:
            # Gérer l'exception si l'utilisateur n'est pas actif
            raise PermissionDenied(str(e))
        except Exception as e:
            # Gestion des autres exceptions
            raise PermissionDenied(f"Erreur lors de la connexion: {str(e)}")
