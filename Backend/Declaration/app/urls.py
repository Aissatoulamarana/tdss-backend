from django_nextjs.views import nextjs_page
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("/nextjs/page", nextjs_page(), name="nextjs_page"),
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
    path('details-declaration/<int:declaration_id>', views.get_declaration_details, name='details-declaration'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)