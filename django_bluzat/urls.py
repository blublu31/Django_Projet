"""
URL configuration for django_bluzat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from gestion_materiel import views
from gestion_materiel.views import accueil, liste_enseignants, ajout_enseignant, liste_salles, liste_accessoires, ajout_salle, liste_materiels

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accueil', accueil, name='accueil'),

    path('enseignants/liste_enseignants', liste_enseignants, name='liste_enseignants'),
    path('enseignants/ajout_enseignant', ajout_enseignant, name='ajout_enseignant'),
    path('enseignants/<int:enseignant_id>/supprimer', views.supprimer_enseignant, name='supprimer_enseignant'),
    path('enseignants/<int:enseignant_id>/materiels_possedes/', views.liste_materiels_possedes, name='liste_materiels_possedes'),
    path('enseignants/<int:enseignant_id>/materiels_proprietaire/', views.liste_materiels_proprietaire, name='liste_materiels_proprietaire'),

    path('salles/liste_salles', liste_salles, name='liste_salles'),
    path('liste_materiels_salle/<int:salle_id>/', views.liste_materiels_salle, name='liste_materiels_salle'),
    path('salles/ajout_salle', ajout_salle, name='ajout_salle'),
    path('salles/supprimer/<int:salle_id>/', views.supprimer_salle, name='supprimer_salle'),

    path('materiel/liste_materiels', liste_materiels, name='liste_materiels'),
    path('materiel/supprimer/<int:materiel_id>/', views.supprimer_materiel, name='supprimer_materiel'),
    path('materiel/ajout_materiel/', views.ajout_materiel, name='ajout_materiel'),

    path('materiel/<int:materiel_id>/accessoires/', liste_accessoires, name='liste_accessoires'),
    path('materiel/<int:materiel_id>/accessoires/supprimer/<int:accessoire_id>', views.supprimer_accessoire, name='supprimer_accessoire'),
    path('materiel/<int:materiel_id>/accessoires/ajouter/', views.ajouter_accessoire_via_materiel, name='ajouter_accessoire'),
    path('materiel/<int:materiel_id>/accessoire/<int:accessoire_id>/modifier/', views.modifier_accessoire, name='modifier_accessoire'),

    path('transfert/choix_materiel', views.choix_materiel, name='choix_materiel'),
    path('transfert/<int:materiel_id>/liste_historique_transferts/', views.liste_historique_transferts, name='liste_historique_transferts'),
    path('transfert/<int:materiel_id>/afficher_transfert/<int:transfert_id>/', views.afficher_transfert,name='afficher_transfert'),
    path('transfert/ajout_transfert/<int:materiel_id>/', views.ajout_transfert, name='ajout_transfert'),
    path('transfert/<int:materiel_id>/supprimer/<int:transfert_id>/', views.supprimer_transfert, name='supprimer_transfert'),
]

