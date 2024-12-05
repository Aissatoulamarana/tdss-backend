from django_nextjs.views import nextjs_page
from django.urls import path
from . import views

urlpatterns = [
    path("/nextjs/page", nextjs_page(), name="nextjs_page"),
    path('api/declarations/', views.list_declarations, name='list_declarations'),
    path('api/declarations/create/', views.create_declaration, name='create_declaration'),
    path('validate-declaration/<int:declaration_id>/', views.validate_declaration, name='validate-declaration'),
    path('list-factures/', views.list_factures, name='list_factures'),
    path('paid-facture/<int:facture_id>/', views.paid_facture, name= 'paid_facture'),
]