from django.db import models
from datetime import datetime
# Create your models here.


class Declaration(models.Model):
    declaration_number = models.CharField(max_length=50, unique=True)
    create_date = models.DateField()
    status = models.CharField(max_length=20, default='draft')  # 'draft' ou 'soumise'
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
