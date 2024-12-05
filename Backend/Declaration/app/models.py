from django.db import models
from datetime import datetime
# Create your models here.


class Declaration(models.Model):
    declaration_number = models.CharField(max_length=50, unique=True)
    create_date = models.DateField()
    status = models.CharField(max_length=20, default='Brouillon')  # 'draft' ou 'soumise'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    numero = models.CharField(max_length=50)
    type = models.CharField(max_length=20, default='Nouvelle')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.type}"

class Facture(models.Model):
    numero_facture = models.CharField(max_length=50, unique=True)
    declaration = models.OneToOneField(Declaration, on_delete=models.CASCADE, related_name='facture')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, default='Non payée')  # 'payée' ou 'non payée'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

