from django_nextjs.views import nextjs_page
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', nextjs_page()),  # Catch-all route for Next.js pages
    # path('<path:path>', nextjs_page()),  # Catch all other dynamic routes
    path('api/declarations/', views.list_declarations, name='list_declarations'),
    path('api/declarations/create/', views.create_declaration, name='create_declaration'),
    path('validate-declaration/<int:declaration_id>/', views.validate_declaration, name='validate-declaration'),
    path('list-factures/', views.list_factures, name='list_factures'),
    path('paid-facture/<int:facture_id>/', views.paid_facture, name= 'paid_facture'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:id>/', views.user_detail, name='user_detail'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:id>/put', views.update_user, name='update_user'),
    path('facturer-declaration/<int:declaration_id>/', views.facturer_declarations, name='facturer-declarations'),
    path('rejeter-declaration/<int:declaration_id>/', views.rejeter_declaration, name='rejeter-declaration'),  
    path('details-declaration/<int:declaration_id>/', views.get_declaration_details, name='details-declaration'),
    path('supprimer-declaration/<int:declaration_id>/', views.supprimer_declaration , name='supprimer-declaration'),
    path('create-fonction/', views.create_fonction, name='create-fonction'),
    path('fonction/<int:function_id>/', views.fonction_detail, name='fonction_detail'),
    path('delete/fonction/<int:function_id>/', views.delete_fonction, name='delete_fonction'),
    path('edit/fonction/<int:function_id>/', views.put_fonction, name='put_fonction'),
    path('list-fonction/', views.list_fonction, name='list_fonction'),
    path('api/move_declaration/', views.move_declaration_items, name='move_declaration'),
    path('bank/create', views.create_bank, name='create_bank'),
    path('list_bank/', views.bank_list, name='list_bank'),
    path('bank/<int:bank_id>/', views.bank_detail, name='bank_detail'),
    path('api/payeur/', views.create_payeur, name='create_payeur'),
    path('login/', views.login_user, name='login'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate-user'),
    path('banni-user/<int:user_id>/', views.bannir_user, name='activate-user'),
    path('me/', views.get_user_info, name='me'),
    path('api/search_passport/', views.search_passport, name='search_passport'),
    path('facture/<int:facture_id>/', views.details_factures, name='details_factures'),
    path('paiements/', views.list_paiements, name='liste_paiements'),
  


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)