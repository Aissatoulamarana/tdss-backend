from django.shortcuts import render
from django.db.models import Count, F
# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Declaration, Item, Facture

@csrf_exempt
def create_declaration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            declaration = Declaration.objects.create(
                declaration_number=data.get('declarationNumber'),
                create_date=data.get('createDate'),
                status=data.get('status', 'draft'),
            )
            items = data.get('items', [])
            for item in items:
                Item.objects.create(
                    declaration=declaration,
                    numero=item['numero'],
                    type=item['type'],
                    fonction=item['fonction'],
                    nationalite=item['nationalite'],
                    prenom=item['prenom'],
                    nom=item['nom'],
                )
                 # Génération de la facture
            montant = Facture.calculate_montant(data.get('type', 'Nouvelle'))
            numero_facture = f"FAC-{declaration.declaration_number}"
            Facture.objects.create(
                numero_facture=numero_facture,
                declaration=declaration,
                montant=montant,
            )
            return JsonResponse({"message": "Declaration created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def list_declarations(request):
    if request.method == "GET":
        # Ajoutez une annotation pour inclure le montant de la facture
        declarations = Declaration.objects.annotate(
            items_count=Count('items'),
            montant_facture=F('facture__montant')  # Utilise la relation avec Facture
        ).values(
            'id', 'declaration_number', 'create_date', 'status', 'items_count', 'montant_facture'
        )

        return JsonResponse(list(declarations), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def validate_declaration(request, declaration_id):
    if request.method == "POST":
        try:
            # Récupérer la déclaration par ID
            declaration = Declaration.objects.get(id=declaration_id)
            # Mettre à jour le statut
            declaration.status = 'validée'
            declaration.save()
            return JsonResponse({"success": True, "message": "Déclaration validée avec succès."})
        except Declaration.DoesNotExist:
            return JsonResponse({"success": False, "error": "Déclaration non trouvée."}, status=404)
    return JsonResponse({"success": False, "error": "Méthode non autorisée."}, status=405)

@csrf_exempt
def paid_facture(request, facture_id):
    if request.method == "POST":
        try:
            facture = Facture.objects.get(id=facture_id)
            facture.statut = 'paid'
            facture.save()
            return JsonResponse({"success": True, "message": "Facture payée avec succès."})
        except Facture.DoesNotExist:
            return JsonResponse({"success": False, "error": "Facture non trouvée."}, status = 404)
    return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status = 404)

def list_factures(request):
    if request.method == "GET":
        factures = Facture.objects.values(
           'id', 'numero_facture', 'declaration__declaration_number', 'montant', 'statut', 'created_at'
        )
        return JsonResponse(list(factures), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)
