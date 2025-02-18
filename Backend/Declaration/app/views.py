
from django.db.models import Count, F
# Create your views here.
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Declaration, Item, Facture, CustomUser, fonction, Bank, Paiement, Payeur
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
import jwt
from django.conf import settings
import random
import string
from datetime import datetime
from django.db.models import Max



@csrf_exempt  # Si vous avez besoin de désactiver temporairement la protection CSRF
def login_user(request):
    if request.method == 'POST':
        try:
            # Charger les données JSON envoyées dans la requête
            data = json.loads(request.body)

            # Récupérer les valeurs des champs
            email = data.get('email')
            password = data.get('password')

            # Vérifier si les champs sont fournis
            if not email or not password:
                return JsonResponse({'error': 'Nom d\'utilisateur et mot de passe sont requis'}, status=400)

            # Utiliser authenticate pour valider l'utilisateur
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Connecter l'utilisateur à la requête
                login(request, user)

                # Génération du token JWT
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Si l'utilisateur est authentifié avec succès
                return JsonResponse({'message': 'Connexion réussie', 'user': email, 'access_token': access_token}, status=200)
            else:
                # Si l'authentification échoue
                return JsonResponse({'error': 'Nom d\'utilisateur ou mot de passe incorrect'}, status=400)

        except PermissionDenied as e:
            # Si l'exception PermissionDenied est levée dans le backend, capturer et renvoyer le message personnalisé
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Erreur lors du traitement du JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Erreur lors de la connexion: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def create_declaration(request):
    if request.method == "POST":
        try:
            # Vérification et extraction du token JWT
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"error": "Utilisateur non authentifié"}, status=401)

            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = CustomUser.objects.get(id=payload["user_id"])
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expiré"}, status=401)
            except jwt.DecodeError:
                return JsonResponse({"error": "Token invalide"}, status=401)
            except CustomUser.DoesNotExist:
                return JsonResponse({"error": "Utilisateur introuvable"}, status=404)

            # Extraction des données textuelles et fichiers
            data = request.POST
            files = request.FILES

            # Création de la déclaration
            declaration = Declaration.objects.create(
                user=user,
                declaration_number=data.get('declarationNumber'),
                create_date=data.get('createDate'),
                status=data.get('status', 'brouillon'),
                type=data.get('type', '').strip()
            )

            total_montant = 0.00

            # Extraction dynamique des items depuis le FormData
            items = []
            index = 0
            while f'items[{index}][numero]' in data:
                items.append({
                    "numero": data.get(f'items[{index}][numero]'),
                    "nom": data.get(f'items[{index}][nom]'),
                    "prenom": data.get(f'items[{index}][prenom]'),
                    "telephone": data.get(f'items[{index}][telephone]'),
                    "fonction": data.get(f'items[{index}][fonction]'),
                    # Les fichiers seront extraits depuis request.FILES
                    "empreinte": files.get(f'items[{index}][empreinte]'),
                    "signature": files.get(f'items[{index}][signature]'),
                    "recto": files.get(f'items[{index}][recto]'),
                    "verso": files.get(f'items[{index}][verso]')
                })
                index += 1

            # Création des éléments associés à la déclaration
            for idx, item in enumerate(items):
                print(f"Fonction recherchée : '{item['fonction']}'")
                try:
                    fonction_instance = fonction.objects.get(name=item['fonction'])
                except fonction.DoesNotExist:
                    return JsonResponse(
                        {"error": f"Fonction '{item['fonction']}' non trouvée dans la base de données."},
                        status=400
                    )

                created_item = Item.objects.create(
                declaration=declaration,
                numero=item['numero'],
                fonction=fonction_instance,
                telephone=item['telephone'],
                prenom=item['prenom'],
                nom=item['nom'],
                empreinte=item['empreinte'],
                signature=item['signature'],
                recto=item['recto'],
                verso=item['verso']
            )

                # Exemple de calcul du montant total
                TARIFS = {
                    'Nouvelle': {
                        'A': 3000.00,
                        'B': 2000.00,
                        'C': 1200.00
                    },
                    'Renouvellement': {
                        'A': 3000.00,
                        'B': 2000.00,
                        'C': 1200.00
                    },
                    'Duplicata': {
                        'A': 3000.00,
                        'B': 2000.00,
                        'C': 1200.00
                    }
                }

                permit = (created_item.permis or '').strip().upper()
                print(f"Item {idx} permis généré : '{permit}'")
                declaration_type = data.get('type', '').strip()
                if declaration_type in TARIFS and permit in TARIFS[declaration_type]:
                    total_montant += TARIFS[declaration_type][permit]
                else:
                    print(f"Aucune correspondance pour type='{declaration_type}' et permis='{permit}'. Montant par défaut = 0.")
                    total_montant += 0.00

            # Mise à jour du montant total sur la déclaration
            declaration.montant = total_montant
            declaration.save()

            return JsonResponse({"message": "Déclaration créée avec succès", "montant": total_montant}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Méthode de requête invalide"}, status=405)



def list_declarations(request):
    if request.method == "GET":
        # Ajoutez une annotation pour inclure le montant de la facture
        declarations = Declaration.objects.annotate(
            items_count=Count('items'),
            montant_facture=F('montant')  # Utilise la relation avec Facture
        ).values(
            'id', 'declaration_number', 'create_date', 'status', 'items_count', 'montant_facture', 
        )

        return JsonResponse(list(declarations), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_declaration_details(request, declaration_id):
    if request.method == "GET":
        try:
            # Récupérer la déclaration
            declaration = Declaration.objects.get(id=declaration_id)
            
            # Récupérer l'utilisateur associé
          
            user_info = {
                    "username": declaration.user.username if declaration.user else None,
                    "email": declaration.user.email if declaration.user else None,
                    "company": declaration.user.company if declaration.user else None,
                    "address": declaration.user.address if declaration.user else None,
                    "telephone": declaration.user.phone_number if declaration.user else None
                }
            
            # Récupérer les éléments associés avec optimisation
            items = Item.objects.filter(declaration=declaration).select_related('fonction').values(
                "numero", "prenom", "nom", "fonction__name", "telephone" ,"fonction__category", "permis"
            )
            
            return JsonResponse({
                "id": declaration.id,
                "declaration_number": declaration.declaration_number,
                "create_date": declaration.create_date.strftime('%Y-%m-%d %H:%M:%S'),  # Format de la date
                "status": declaration.status,
                "user": user_info,  # Ajouter l'utilisateur
                'type': declaration.type,
                "items": list(items),  # Inclure les éléments associés
            }, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Déclaration non trouvée"}, status=404)

    return JsonResponse({"error": "Méthode de requête invalide"}, status=405)


def details_factures(request, facture_id):
    if request.method == 'GET':
        try:
            # Récupère la facture par son ID
            facture = Facture.objects.get(id=facture_id)
        except Facture.DoesNotExist:
            return JsonResponse({"error": "Facture non trouvée."}, status=404)

        # Récupération du payeur s'il existe
        if facture.payeur is not None:
            payeur = facture.payeur
            payeur_data = {
                'nom': payeur.nom,
                'prenom': payeur.prenom,
                'email': payeur.email,
                'telephone': payeur.telephone,
                'pays': payeur.pays,
                'date_enregistrement': payeur.date_enregistrement,
                'numero_compte': payeur.numero_compte,
            }
        else:
            payeur_data = None

        # Récupération de l'utilisateur s'il existe
        user = facture.declaration.user
        if user is not None:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'country': user.country,
                'address': user.address,
                'company': user.company,
                'role': user.role,
                'profile_image': user.profile_image.url if user.profile_image else None,
                'status': user.status,
            }
        else:
            user_data = None

        # Récupérer les items associés à la déclaration
        items = facture.declaration.items.all()

        # Définition des tarifs (fixes comme dans ton exemple)
        TARIFS = {
            'Nouvelle': {'A': 3600.00, 'B': 2200.00, 'C': 1200.00},
            'Renouvellement': {'A': 3000.00, 'B': 1800.00, 'C': 1000.00},
            'Duplicata': {'A': 1500.00, 'B': 1000.00, 'C': 500.00}
        }

        # Dictionnaire pour stocker la somme des quantités pour chaque permis
        permis_quantite = {'A': 0, 'B': 0, 'C': 0}

        # Liste pour les détails des catégories
        details_categories = []

        # Comptage des permis et ajout dans le tableau
        for item in items:
            permis = item.permis  # "A", "B", ou "C"
            # type_permis = item.type  # "Renouvellement", "Duplicata", ou "Nouvelle"

            # Si le permis est valide (A, B, ou C), incrémenter le compteur
            if permis in permis_quantite:
                permis_quantite[permis] += 1  # Ajouter 1 pour chaque occurrence du permis

        # Créer un seul dictionnaire par type de permis avec la quantité
        for permis, quantite in permis_quantite.items():
            if quantite > 0:  # N'ajouter que si la quantité est > 0
                # Trouver le prix unitaire pour ce permis
                prix_unitaire = 0.00
                type_permis = facture.declaration.type  # "Renouvellement", "Duplicata", ou "Nouvelle"
                for item in items:
                    if item.permis == permis:
                       
                        prix_unitaire = TARIFS.get(type_permis, {}).get(permis, 0.00)
                        break

                # Ajouter les détails dans le tableau
                details_categories.append({
                    'permis': permis,
                    'quantite': quantite,
                    'prix_unitaire': prix_unitaire,
                    'category': item.fonction.category if item.fonction and item.fonction.category else None  # Catégorie de la fonction
                })

        # Préparer la réponse JSON avec les données
        response_data = {
            'id': facture.id,
            'numero_facture': facture.numero_facture,
            'declaration_number': facture.declaration.declaration_number if facture.declaration else None,
            'create_date': facture.created_at,
            'montant_gnf': facture.montant_gnf,
            'montant_usd': facture.montant_usd,
            'statut': facture.statut,
            'payeur': payeur_data,
            'client': user_data,
            'dec_date': facture.declaration.created_at,
            'details': details_categories,  # Détails des items avec quantités spécifiques
        }

        return JsonResponse(response_data)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)



@csrf_exempt
def validate_declaration(request, declaration_id):
    if request.method == "POST":
        try:
            # Récupérer la déclaration par ID
            declaration = Declaration.objects.get(id=declaration_id)

            if declaration.status == 'validée':
                return JsonResponse({
                    "success": False,
                    "error": "La déclaration a déjà été validée."
                }, status=400)
            # Mettre à jour le statut

            declaration.status = 'validée'
            declaration.save()
            
           

            return JsonResponse({"success": True, "message": "Déclaration validée avec succès."})
        except Declaration.DoesNotExist:
            return JsonResponse({"success": False, "error": "Déclaration non trouvée."}, status=404)
    return JsonResponse({"success": False, "error": "Méthode non autorisée."}, status=405)

@csrf_exempt
def facturer_declarations(request, declaration_id):
    if request.method == 'POST':
        try:
            # Récupérer la déclaration par ID
            declaration = Declaration.objects.get(id=declaration_id)
            print(f"Déclaration trouvée : {declaration}")

            # Vérification que la déclaration n'a pas déjà été facturée
            if declaration.status == 'facturée':
                return JsonResponse({
                    "success": False,
                    "error": "La déclaration a déjà été facturée."
                }, status=400)

            # Utiliser directement le montant de la déclaration
            montant_usd = declaration.montant
            print(f"Montant de la déclaration : {montant_usd}")

            now = datetime.now()
            year = now.year
            month = now.month 

            # Récupérer la dernière facture du mois et incrémenter la séquence
            last_facture = Facture.objects.filter(numero_facture__startswith=f"FCT-{year}-{month:02d}-").aggregate(Max('numero_facture'))

            if last_facture['numero_facture__max']:
                last_sequence = int(last_facture['numero_facture__max'].split('-')[-1])
            else:
                last_sequence = 0

            next_sequence = last_sequence + 1

            # Génération du numéro de facture unique
            numero_facture = f"FCT-{year}-{month:02d}-{next_sequence:03d}"

            # Création de la facture avec le même montant que la déclaration
            facture = Facture.objects.create(
                numero_facture=numero_facture,
                declaration=declaration,
                montant_usd=montant_usd
            )

            # Mettre à jour le statut de la déclaration à 'facturée'
            declaration.status = 'facturée'
            declaration.save()

            return JsonResponse({
                "success": True,
                "message": "Déclaration facturée avec succès.",
                "facture": {
                    "numero": facture.numero_facture,
                    "montant": facture.montant_usd,
                }
            })

        except Declaration.DoesNotExist:
            return JsonResponse({"success": False, "error": "Déclaration non trouvée."}, status=404)
        except Exception as e:
            return JsonResponse({
                "success": False, 
                "error": "Une erreur est survenue lors de la facturation.",
                "details": str(e)
            }, status=500)

    return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)



@csrf_exempt
def rejeter_declaration(request, declaration_id):
    if request.method == "POST":
        try:
            # Vérifier si l'ID est valide
            declaration_id = int(declaration_id)
            # Récupérer la déclaration par ID
            declaration = Declaration.objects.get(id=declaration_id)
            # Mettre à jour le statut
            declaration.status = 'rejetée'
            declaration.save()
            return JsonResponse({"success": True, "message": "Déclaration rejetée avec succès."})
        except ValueError:
            return JsonResponse({"success": False, "error": "ID de déclaration invalide."}, status=400)
        except Declaration.DoesNotExist:
            return JsonResponse({"success": False, "error": "Déclaration non trouvée."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def supprimer_declaration(request, declaration_id):
    if request.method == 'DELETE':
        try:
            # Récupérer la déclaration par son ID
            declaration = Declaration.objects.get(id=declaration_id)
            
            # Supprimer la déclaration
            declaration.delete()
            
            return JsonResponse({"success": True, "message": "Déclaration supprimée avec succès."})
        
        except Declaration.DoesNotExist:
            return JsonResponse({"success": False, "error": "Déclaration non trouvée."}, status=404)
        
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    
    return JsonResponse({"success": False, "error": "Méthode non autorisée."}, status=405)


@csrf_exempt
def paid_facture(request, facture_id):
    if request.method == "POST":
        try:
            # Récupération de la facture
            facture = Facture.objects.get(id=facture_id)

            if not facture.payeur:
                return JsonResponse({"success": False, "error": "Aucun payeur associé à la facture."}, status=400)

            # Vérification et extraction du token JWT
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"error": "Utilisateur non authentifié"}, status=401)

            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = CustomUser.objects.get(id=payload["user_id"])
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expiré"}, status=401)
            except jwt.DecodeError:
                return JsonResponse({"error": "Token invalide"}, status=401)
            except CustomUser.DoesNotExist:
                return JsonResponse({"error": "Utilisateur introuvable"}, status=404)

            # Récupération des données envoyées
            try:
                data = json.loads(request.body)
                banque_id = data.get('banque_id')
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "error": "Format de données invalide."}, status=400)

            # Vérifier si la banque existe
            try:
                bank = Bank.objects.get(id=banque_id, is_active=True)
            except Bank.DoesNotExist:
                return JsonResponse({"success": False, "error": "Banque invalide ou non disponible."}, status=400)

            # Création du paiement
            paiement = Paiement.objects.create(
                facture=facture,
                banque=bank,
                utilisateur=user,  # Utilisation correcte de l'utilisateur authentifié
            )

            if facture.statut == 'paid':
                return JsonResponse({
                    "success": False,
                    "error": "La facture a déjà été payée."
                }, status=400)

            # Mise à jour du statut de la facture
            facture.statut = 'paid'
            facture.save()

            return JsonResponse({
                "success": True,
                "message": "Facture payée avec succès.",
                "paiement_id": paiement.id
            }, status=201)  # 201 Created

        except Facture.DoesNotExist:
            return JsonResponse({"success": False, "error": "Facture non trouvée."}, status=404)

    return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)



@csrf_exempt
def paid_factures(request):
    if request.method == "POST":
        try:
            # Vérification et extraction du token JWT
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"error": "Utilisateur non authentifié"}, status=401)
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = CustomUser.objects.get(id=payload["user_id"])
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expiré"}, status=401)
            except jwt.DecodeError:
                return JsonResponse({"error": "Token invalide"}, status=401)
            except CustomUser.DoesNotExist:
                return JsonResponse({"error": "Utilisateur introuvable"}, status=404)

            # Récupération et décodage des données JSON envoyées
            try:
                data = json.loads(request.body)
                facture_ids = data.get("facture_ids", [])
                banque_id = data.get("banque_id")
            except json.JSONDecodeError:
                return JsonResponse({"error": "Format de données invalide."}, status=400)

            if not facture_ids or not isinstance(facture_ids, list):
                return JsonResponse({"error": "La liste des facture_ids est requise."}, status=400)

            # Vérifier l'existence de la banque et qu'elle est active
            try:
                bank = Bank.objects.get(id=banque_id, is_active=True)
            except Bank.DoesNotExist:
                return JsonResponse({"error": "Banque invalide ou non disponible."}, status=400)

            paiements_created = []
            erreurs = []

            # Parcours de chaque facture dans la liste
            for facture_id in facture_ids:
                try:
                    facture = Facture.objects.get(id=facture_id)
                except Facture.DoesNotExist:
                    erreurs.append(f"Facture {facture_id} non trouvée.")
                    continue

                if not facture.payeur:
                    erreurs.append(f"Aucun payeur associé à la facture {facture_id}.")
                    continue

                if facture.statut == "paid":
                    erreurs.append(f"La facture {facture_id} a déjà été payée.")
                    continue

                # Création du paiement pour la facture
                paiement = Paiement.objects.create(
                    facture=facture,
                    banque=bank,
                    utilisateur=user  # Utilisateur authentifié
                )

                # Mise à jour du statut de la facture en "paid"
                facture.statut = "paid"
                facture.save()

                paiements_created.append(paiement.id)

            # Préparation de la réponse
            response_data = {
                "success": True,
                "paiements_created": paiements_created,
            }
            if erreurs:
                response_data["erreurs"] = erreurs

            return JsonResponse(response_data, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


def list_paiements(request):
    if request.method == "GET":
        # Récupération de tous les paiements avec leurs objets liés pour éviter des requêtes supplémentaires
        paiements = Paiement.objects.all().select_related(
            'facture', 'facture__declaration', 'facture__payeur', 'banque', 'utilisateur'
        )
        
        paiements_data = []
        for paiement in paiements:
            facture = paiement.facture
            
            # Récupérer le numéro de déclaration s'il existe
            declaration_number = facture.declaration.declaration_number if facture.declaration else None
            # Récupérer le nom de la banque
            bank_name = paiement.banque.name if paiement.banque else None
            # Récupérer la date du paiement
            date_paiement = paiement.created
            montantGnf = facture.montant_gnf
            montantUsd = facture.montant_usd
            type_dec = facture.declaration.type
            
            # Déterminer le nom et le prénom à afficher :
            # Si la facture possède un payeur, on utilise ses informations.
            # Sinon, on utilise les informations de l'utilisateur qui a effectué le paiement.
            if facture.payeur is not None:
                payer_nom = facture.payeur.nom
                payer_prenom = facture.payeur.prenom
            elif paiement.utilisateur is not None:
                # On essaye d'utiliser first_name et last_name s'ils existent, sinon username pour le nom.
                payer_nom = getattr(paiement.utilisateur, 'first_name', None) or paiement.utilisateur.username
                payer_prenom = getattr(paiement.utilisateur, 'last_name', None) or ""
            else:
                payer_nom = ""
                payer_prenom = ""
            
            paiements_data.append({
                "numero_facture": facture.numero_facture,
                "declaration_number": declaration_number,
                "date_paiement": date_paiement,
                "bank_name": bank_name,
                "payer_nom": payer_nom,
                "payer_prenom": payer_prenom,
                "montantGN": montantGnf,
                "montantUsd": montantUsd,
                "type": type_dec
            })
        
        return JsonResponse(paiements_data, safe=False)
    
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


def list_factures(request):
    if request.method == "GET":
        factures = Facture.objects.values(
           'id', 'numero_facture', 'declaration__declaration_number', 'montant_usd', 'statut', 'created_at', 'montant_gnf'
        )
        return JsonResponse(list(factures), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)





# Liste des utilisateurs
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all().values('id', 'username', 'email', 'phone_number', 'country', 'address', 'company', 'role', 'profile_image', 'status', )
        return JsonResponse(list(users), safe=False)

#Listes des fonctions 
@csrf_exempt
def list_fonction(request):
    fonctions = fonction.objects.all().values('id', 'name', 'category', 'created_at')
    
    # Ajout de number_person à chaque fonction
    fonctions_with_counts = []
    for f in fonctions:
        fonction_obj = fonction.objects.get(id=f['id'])
        count = Item.objects.filter(fonction=fonction_obj).count()
        f['number_person'] = count
        fonctions_with_counts.append(f)

    return JsonResponse({'fonctions': fonctions_with_counts}, safe=False)

# Détails d'un utilisateur
def user_detail(request, id):
    try:
        user = CustomUser.objects.values('id', 'username', 'email', 'phone_number', 'country', 'address', 'company', 'role').get(id=id)
        return JsonResponse(user, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)

# Créer un utilisateur
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            # Charger les données JSON
            data = json.loads(request.body)

            # Récupérer et valider les champs requis
            username=data.get('name')
            email=data.get('email')
            phone_number=data.get('phoneNumber')
            country=data.get('country')
            address=data.get('address')
            company=data.get('company')
            role=data.get('role')
            password=data.get('password')
            profile_image = request.FILES.get('profile_image')

            # Vérification des champs obligatoires
            required_fields = [username, email, password, role]
            if not all(required_fields):
                return JsonResponse({'error': 'Tous les champs obligatoires doivent être remplis'}, status=400)
            # Validation de l'email
            if not email or '@' not in email:
                return JsonResponse({'error': 'Veuillez fournir une adresse email valide'}, status=400)

            # Vérifier si le nom d'utilisateur existe déjà
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Le nom d\'utilisateur est déjà pris'}, status=400)

            # Vérifier si l'email existe déjà
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Cette adresse email est déjà utilisée'}, status=400)

            # Créer l'utilisateur
            user = CustomUser(
                username=username,
                phone_number=phone_number,
                email=email,
                role=role,
                country=country,
                address=address,
                company=company,
                profile_image=profile_image

               
            )

            # Hachage du mot de passe avant de sauvegarder
            user.set_password(password)
            user.save()

            return JsonResponse({'message': 'Utilisateur créé avec succès'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Erreur de format JSON invalide'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': f'Erreur de validation : {str(e)}'}, status=400)
        except Exception as e:
            # Ajout d'un logging pour déboguer les erreurs serveur
            print(f"Erreur inattendue : {str(e)}")  # Remplace par un logger en prod
            return JsonResponse({'error': 'Une erreur est survenue lors de la création de l\'utilisateur'}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt 
def create_payeur(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Création de l'objet Payeur
            payeur = Payeur.objects.create(
                nom=data.get('nom'),
                prenom=data.get('prenom'),
                email=data.get('email'),
                telephone=data.get('telephone'),
                pays=data.get('pays'),
                numero_compte=data.get('numero_compte'),
                devise=data.get('devise'),
            )
            # Facultatif : sauvegarde explicite (create() sauvegarde déjà)
            payeur.save()

            # Récupération de facture_id qui peut être une liste ou un entier
            facture_ids = data.get('facture_id')
            if facture_ids:
                # Si facture_ids est une liste
                if isinstance(facture_ids, list):
                    for fid in facture_ids:
                        try:
                            facture = Facture.objects.get(id=fid)
                            facture.payeur = payeur
                            facture.save()
                        except Facture.DoesNotExist:
                            return JsonResponse({'error': f'La facture avec l\'id {fid} n\'existe pas.'}, status=404)
                        except Exception as e:
                            return JsonResponse({'error': f'Erreur lors de l\'association du payeur à la facture: {str(e)}'}, status=400)
                # Si facture_ids est un entier
                else:
                    try:
                        facture = Facture.objects.get(id=facture_ids)
                        facture.payeur = payeur
                        facture.save()
                    except Facture.DoesNotExist:
                        return JsonResponse({'error': f'La facture avec l\'id {facture_ids} n\'existe pas.'}, status=404)
                    except Exception as e:
                        return JsonResponse({'error': f'Erreur lors de l\'association du payeur à la facture: {str(e)}'}, status=400)

            return JsonResponse({
                'message': 'Payeur créé et associé avec succès',
                'payeur_id': payeur.id,
                'facture_id': facture_ids,
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)




# Supprimer un utilisateur
@csrf_exempt
def delete_user(request, id):
    if request.method == 'DELETE':
        try:
            user = CustomUser.objects.get(id=id)
            user.delete()
            return JsonResponse({'message': 'Utilisateur supprimé avec succès'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)

    
@csrf_exempt
def update_user(request, id):
    if request.method == 'PUT':
        try:
            user = get_object_or_404(CustomUser, id=id)
            data = json.loads(request.body.decode('utf-8'))
            
            # Mise à jour des champs
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'phone_number' in data:
                user.phone_number = data['phone_number']
            if 'country' in data:
                user.country = data['country']
            if 'address' in data:
                user.address = data['address']
            if 'company' in data:
                user.company = data['company']
            if 'role' in data:
                user.role = data['role']

            user.save()  # Enregistrer les modifications
            return JsonResponse({'message': 'User updated successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

        
#Créer une fonction 
@csrf_exempt
def create_fonction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Fonction = fonction.objects.create(
                name=data.get('name'),
                category=data.get('category'),
            )
            Fonction.save()
            return JsonResponse({'message': 'Fonction créé avec succès'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

#Voir details d'une fonction
def fonction_detail(request, function_id):
    """
    Vue qui renvoie les détails d'une fonction avec le nombre de personnes associées.
    """
    if request.method == "GET":
        try:
            function_details = fonction.get_person_count_for_function(function_id)
            return JsonResponse({"data": function_details}, status=200)
        except fonction.DoesNotExist:
            return JsonResponse({"error": "Fonction non trouvée"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
#Supprimer une fonction
@csrf_exempt
def delete_fonction(request, function_id):
    if request.method == "DELETE":
        try:
            function = fonction.objects.get(id = function_id)
            function.delete()
            return JsonResponse({"message": "Fonction supprimée avec succès"}, status=200)
        except fonction.DoesNotExist:
            return JsonResponse({"error": "Fonction non trouvée"}, status=404)
        
#Modifier Une fonction
@csrf_exempt
def put_fonction(request, function_id):
    if request.method == "PUT":
        try:
            function = fonction.objects.get(id=function_id)
            data = json.loads(request.body.decode('utf-8'))

            if 'name' in data:
                function.name = data['title']
            if 'category' in data:
                function.category = data['category']
            function.save()
            return JsonResponse({'message': 'Fonction updated successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        


@csrf_exempt
def move_declaration_items(request):
    if request.method == 'POST':
        try:
            # Parse le corps de la requête
            data = json.loads(request.body)
            
            # Liste des IDs des personnes sélectionnées
            selected_ids = data.get('selected_ids', [])
            # ID de la déclaration cible
            target_declaration_number = data.get('target_declaration', None)

            if not selected_ids or not target_declaration_number:
                return JsonResponse({'error': 'Données invalides ou incomplètes.'}, status=400)
            
            # Récupère la déclaration cible
            target_declaration = get_object_or_404(Declaration, declaration_number=target_declaration_number)
            
            # Met à jour les enregistrements sélectionnés
            updated_count = Item.objects.filter(numero__in=selected_ids).update(declaration=target_declaration)

            return JsonResponse({
                'message': f'{updated_count} éléments déplacés vers la déclaration {target_declaration_number}.',
                'target_declaration': target_declaration_number,
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format JSON invalide.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)
    

@csrf_exempt
def create_bank(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            identifier = data.get('identifier')
            swift_code = data.get('swift_code', None)
           

            if not name or not identifier :
                return JsonResponse(
                    {'error': 'Les champs name, identifier et account_number sont obligatoires.'},
                    status=400
                )
             # Vérification si la banque existe déjà (par name ou identifier)
            if Bank.objects.filter(name=name).exists():
                return JsonResponse(
                    {'error': f'Une banque avec le nom "{name}" existe déjà.'},
                    status=400
                )
            
            if Bank.objects.filter(identifier=identifier).exists():
                return JsonResponse(
                    {'error': f'Une banque avec l’identifiant "{identifier}" existe déjà.'},
                    status=400
                )


            # Création de la banque
            bank = Bank.objects.create(
                name=name,
                identifier=identifier,
                swift_code=swift_code,
                
            )

            # Si un fichier est inclus dans la requête
            if request.FILES.get('logo'):
                logo_file = request.FILES['logo']
                bank.logo.save(logo_file.name, logo_file)

            return JsonResponse(
                {'message': 'Banque créée avec succès.', 'bank_id': bank.id},
                status=201
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Données JSON invalides.'},
                status=400
            )

    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)

def bank_list(request):
    if request.method == 'GET':
        bank = Bank.objects.all().values('id', 'name', 'identifier', 'swift_code', 'logo', 'is_active',  )
        return JsonResponse(list(bank), safe=False)

def bank_detail(request, id):
    try:
        bank = CustomUser.objects.values('id', 'name', 'identifier', 'swift_code', 'logo', 'is_active' ).get(id=id)
        return JsonResponse(bank, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Banque non trouvée'}, status=404)
    





def get_user_info(request):
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "Token manquant ou invalide"}, status=401)
    
    token = auth_header.split(" ")[1]  # Extraction du token

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = CustomUser.objects.get(id=payload["user_id"])  # Récupération de l'utilisateur

        # Vérifier si l'image de profil existe et récupérer son URL
        profile_image_url = user.profile_image.url if user.profile_image else None
        
        return JsonResponse({
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "company": user.company,
                "role": user.role,
                "phone_number": user.phone_number,
                "address": user.address,
                "country": user.country,
                "status": user.status,
                "profile_image": profile_image_url,
            }
        }, status=200)
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expiré"}, status=401)
    except jwt.DecodeError:
        return JsonResponse({"error": "Token invalide"}, status=401)
    except user.DoesNotExist:
        return JsonResponse({"error": "Utilisateur introuvable"}, status=404)


@csrf_exempt
def activate_user(request, user_id):
    if request.method == 'POST':
        try:
            # Vérifier si l'utilisateur existe
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': "Utilisateur introuvable."}, status=404)

            # Vérifier si le compte est déjà actif
            if user.status == 'actif':
                return JsonResponse({'message': "Le compte est déjà actif."}, status=200)

            # Activer le compte
            user.status = 'actif'
            user.save()

            return JsonResponse({'message': "Le compte a été activé avec succès."}, status=200)

        except Exception as e:
            return JsonResponse({'error': f"Erreur lors de l'activation du compte: {str(e)}"}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def bannir_user(request, user_id):
    if request.method == 'POST':
        try:
            # Vérifier si l'utilisateur existe
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': "Utilisateur introuvable."}, status=404)

            # Vérifier si le compte est déjà actif
            if user.status == 'Banni':
                return JsonResponse({'message': "Le compte est déjà banni."}, status=200)

            # Activer le compte
            user.status = 'Banni'
            user.save()

            return JsonResponse({'message': "Le compte a été banni avec succès."}, status=200)

        except Exception as e:
            return JsonResponse({'error': f"Erreur lors du bannissement du compte: {str(e)}"}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def search_passport(request):
    """
    Endpoint pour vérifier l'existence d'un passeport.
    On attend une requête GET avec le paramètre 'numero' correspondant au numéro de passeport.
    """
    # Vérification manuelle de la méthode HTTP
    if request.method != 'GET':
        return JsonResponse(
            {"error": "Méthode non autorisée. Seules les requêtes GET sont acceptées."},
            status=405
        )

    # Récupération manuelle du paramètre 'numero'
    numero = request.GET.get('numero')
    if not numero:
        return JsonResponse(
            {"error": "Le paramètre 'numero' est requis."},
            status=400
        )

    try:
        # Vérifier si un item avec ce numéro de passeport existe
        exists = Item.objects.filter(numero=numero).exists()
        return JsonResponse({"exists": exists})
    except Exception as e:
        # En cas d'erreur, renvoyer une réponse avec le message d'erreur
        return JsonResponse(
            {"error": f"Une erreur est survenue : {str(e)}"},
            status=500
        )
    
@csrf_exempt
def upload_images(request):
    if request.method == 'POST' and request.FILES:
        uploaded_files = request.FILES
        file_urls = {}

        for file_key, file in uploaded_files.items():
            file_path = f"photo_user/{file.name}"
            saved_path = default_storage.save(file_path, ContentFile(file.read()))
            file_urls[file_key] = default_storage.url(saved_path)

        return JsonResponse({"message": "Images uploaded successfully", "file_urls": file_urls}, status=201)

    return JsonResponse({"message": "No images provided", "file_urls": {}}, status=200)
