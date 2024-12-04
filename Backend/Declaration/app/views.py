from django.shortcuts import render
from django.db.models import Count
# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Declaration, Item

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
            return JsonResponse({"message": "Declaration created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def list_declarations(request):
    if request.method == "GET":
        declarations = Declaration.objects.annotate(items_count=Count('items')).values('id', 'declaration_number', 'create_date', 'status', 'items_count')
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