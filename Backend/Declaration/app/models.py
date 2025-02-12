from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import Count

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
    create_date = models.DateField()
    status = models.CharField(max_length=20, default='Brouillon')  # 'draft' ou 'soumise'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    company= models.CharField(max_length=50 , blank=True , null=True)

    def save(self, *args, **kwargs):
        if isinstance(self.create_date, str):
            try:
                self.create_date = datetime.strptime(self.create_date, '%Y-%m-%dT%H:%M:%S%z').date()
            except ValueError:
                pass  # Vous pouvez gérer le format incorrect ici
        super().save(*args, **kwargs)

    def __str__(self):
        return self.declaration_number


class Item(models.Model):
    declaration = models.ForeignKey(Declaration, related_name='items', on_delete=models.CASCADE)
    fonction = models.ForeignKey(fonction, related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    numero = models.CharField(max_length=50)
    type = models.CharField(max_length=20, default='Nouvelle')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=100)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    permis = models.CharField(max_length=1, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Si la fonction est définie, on détermine le type de permis en fonction de sa catégorie
        if self.fonction:
            # On travaille en minuscule pour éviter les problèmes de casse
            category = self.fonction.category.lower() if self.fonction.category else ""
            if category == 'cadres':
                self.type_permis = 'A'
            elif category == 'agent':
                self.type_permis = 'B'
            elif category == 'ouvrier':
                self.type_permis = 'C'
            else:
                # Si la catégorie ne correspond pas à l'une des trois, on peut la laisser vide ou y mettre une valeur par défaut
                self.type_permis = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.type}"



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
    user= models.ForeignKey(CustomUser, on_delete=models.PROTECT , blank=True, null=True)
    numero_facture = models.CharField(max_length=50, unique=True)
    declaration = models.OneToOneField(Declaration, on_delete=models.CASCADE, related_name='facture')
    montant_usd = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, default='En attente')  # 'payée' ou 'non payée'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payeur = models.ForeignKey(Payeur, on_delete=models.SET_NULL, null=True, blank=True)
    montant_gnf = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Taux de conversion fixe : 1 USD = 10 000 GNF
        taux_conversion = 10000  
        self.montant_gnf = self.montant_usd * taux_conversion
        super().save(*args, **kwargs)

    @staticmethod
    def calculate_montant(declaration_type):
        tarifs = {
            'Nouvelle': 100.00,      # Montant pour une nouvelle déclaration
            'Renouvellement': 50.00, # Montant pour un renouvellement
            'Duplicata': 30.00       # Montant pour un duplicata
        }
        return tarifs.get(declaration_type, 0.00)  # Par défaut, 0 si le type n'est pas trouvé

    def __str__(self):
        return f"Facture {self.numero_facture} - {self.montant} {self.statut}"

class Paiement(models.Model):
    facture = models.OneToOneField(Facture, on_delete=models.CASCADE , related_name='paiement')
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banque = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='paiements') 
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.PROTECT,  null=True, blank=True)
    def __str__(self):
        return f"Paiement pour {self.facture.numero_facture} via {self.banque}"




