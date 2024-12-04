from django_nextjs.views import nextjs_page
from django.urls import path
from . import views

urlpatterns = [
    path("/nextjs/page", nextjs_page(), name="nextjs_page"),
    path('api/declarations/', views.list_declarations, name='list_declarations'),
    path('api/declarations/create/', views.create_declaration, name='create_declaration'),
    
]