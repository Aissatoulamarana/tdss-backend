from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import Count
import random
import string

# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, default='inactif')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Nouveau related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Nouveau related_name
        blank=True
    )



class fonction(models.Model):
    name = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_person_count_for_function(function_id):
        """
        Retourne le nombre de personnes associées à une fonction spécifique.
        """
        from .models import Item  # Assurez-vous que Item est correctement lié à Fonction

        # Récupère la fonction et le nombre d'items associés à cette fonction
        fonction_obj = fonction.objects.get(id=function_id)

        # Compter le nombre de personnes associées à cette fonction
        count = Item.objects.filter(fonction=fonction_obj).count()

        return {
            'id': fonction_obj.id,
            'name': fonction_obj.name,
            'category': fonction_obj.category,
            'date': fonction_obj.created_at,
            'number_person': count
        }


class Bank(models.Model):
    name = models.CharField(max_length=100)  # Nom de la banque
    identifier = models.CharField(max_length=50, unique=True)  # Identifiant unique
    swift_code = models.CharField(max_length=50, blank=True, null=True)  # Code SWIFT
    logo = models.ImageField(upload_to="bank_logos/", blank=True, null=True)  # Logo de la banque
    is_active = models.BooleanField(default=True)  # Statut actif/inactif
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Declaration(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=True, null=True)
    declaration_number = models.CharField(max_length=50, unique=True)
    # create_date = models.DateField()
    type = models.CharField(max_length=50 , default='Nouvelle')
    status = models.CharField(max_length=20, default='Brouillon')  # 'draft' ou 'soumise'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    company= models.CharField(max_length=50 , blank=True , null=True)

    # def save(self, *args, **kwargs):
    #     if isinstance(self.create_date, str):
    #         try:
    #             self.create_date = datetime.strptime(self.create_date, '%Y-%m-%dT%H:%M:%S%z').date()
    #         except ValueError:
    #             pass  # Vous pouvez gérer le format incorrect ici
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.declaration_number


class Item(models.Model):
    declaration = models.ForeignKey('Declaration', related_name='items', on_delete=models.CASCADE)
    fonction = models.ForeignKey('fonction', related_name='items', on_delete=models.CASCADE)
    numero = models.CharField(max_length=50)
    identifier = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    empreinte = models.ImageField(upload_to="photo_user/", blank=True, null=True)
    signature = models.ImageField(upload_to="photo_user/", blank=True, null=True)
    recto = models.ImageField(upload_to="photo_user/", blank=True, null=True)
    verso = models.ImageField(upload_to="photo_user/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    permis = models.CharField(max_length=1, blank=True, null=False)

    def save(self, *args, **kwargs):
        # Log de debug pour vérifier la fonction et sa catégorie
        print(f"Fonction: {self.fonction}, Catégorie: {self.fonction.category}")
        
        if self.fonction:
            category = self.fonction.category.lower() if self.fonction.category else ""
            print(f"Catégorie traitée: {category}")
            
            if category == 'cadres':
                self.permis = 'A'
            elif category == 'agent':
                self.permis = 'B'
            elif category == 'ouvrier':
                self.permis = 'C'
            else:
                self.permis = None

        # Génération de l'identifiant unique s'il n'est pas déjà défini
        if not self.identifier:
            # Récupérer le dernier item créé (en se basant sur l'id)
            last_item = Item.objects.order_by('-id').first()
            if last_item and last_item.identifier:
                try:
                    # On extrait la partie numérique en supposant le format "ID" suivi de 4 chiffres puis 6 caractères aléatoires
                    numeric_part = int(last_item.identifier[2:6])
                except (ValueError, IndexError):
                    numeric_part = 0
            else:
                numeric_part = 0

            numeric_part += 1
            padded_numeric = str(numeric_part).zfill(4)
            # Générer une chaîne aléatoire de 6 caractères en mélangeant chiffres et lettres majuscules
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.identifier = f"ID{padded_numeric}{random_part}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.identifier} - {self.nom} {self.prenom}"



class Payeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    devise = models.CharField(max_length=50, )
    pays = models.CharField(max_length=50, null=True, blank=True)
    numero_compte = models.CharField(max_length=50, unique=True)
    date_enregistrement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Facture(models.Model):
    numero_facture = models.CharField(max_length=50, unique=True)
    declaration = models.OneToOneField(Declaration, on_delete=models.CASCADE, related_name='facture')
    montant_usd = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, default='En attente')  # 'payée' ou 'non payée'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payeur = models.ForeignKey(Payeur, on_delete=models.SET_NULL, null=True, blank=True)
    montant_gnf = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Vérifier si la déclaration existe et a un montant
        if self.declaration:
            self.montant_usd = self.declaration.montant  # Récupération du montant de la déclaration

        # Taux de conversion fixe (1 USD = 9200 GNF)
        taux_conversion = 9200  
        self.montant_gnf = self.montant_usd * taux_conversion

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Facture {self.numero_facture} - {self.montant_usd} {self.statut}"

class Paiement(models.Model):
    facture = models.OneToOneField(Facture, on_delete=models.CASCADE , related_name='paiement')
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banque = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='paiements') 
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.PROTECT,  null=True, blank=True)
    def __str__(self):
        return f"Paiement pour {self.facture.numero_facture} via {self.banque}"




