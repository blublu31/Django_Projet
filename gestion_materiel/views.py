from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Enseignant, Materiel, AccessoireMateriel, TransfertMateriel, Salle, TransfertAccessoire
from .forms import EnseignantForm, SalleForm, AccessoireViaMaterielForm, MaterielForm, AccessoireFormSet, TransfertForm
from django.contrib import messages

def accueil(request):
    return render(request, 'gestion_materiel/accueil.html')

"""enseignants"""
def liste_enseignants(request):
    enseignants = Enseignant.objects.all()
    return render(request, 'gestion_materiel/enseignants/liste_enseignants.html', {'enseignants': enseignants})

def ajout_enseignant(request):
    if request.method == 'POST':
        form = EnseignantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enseignant ajouté avec succès')
            return redirect('liste_enseignants')
    else:
        form = EnseignantForm()
    return render(request, 'gestion_materiel/enseignants/ajout_enseignant.html', {'form': form})


def liste_materiels_possedes(request, enseignant_id):
    enseignant = Enseignant.objects.get(id=enseignant_id)

    materiels = Materiel.objects.filter(Q(possesseur__nom__icontains=enseignant.nom) & Q(possesseur__prenom__icontains=enseignant.prenom))

    context = {
        'enseignants': enseignant,
        'materiels': materiels,
    }

    return render(request, 'gestion_materiel/enseignants/liste_materiels_possedes.html', context)


def liste_materiels_proprietaire(request, enseignant_id):
    enseignant = Enseignant.objects.get(id=enseignant_id)

    materiels = Materiel.objects.filter(Q(proprietaire__nom__icontains=enseignant.nom) & Q(proprietaire__prenom__icontains=enseignant.prenom))

    context = {
        'enseignants': enseignant,
        'materiels': materiels,
    }

    return render(request, 'gestion_materiel/enseignants/liste_materiels_proprietaire.html', context)

def supprimer_enseignant(request, enseignant_id):
    if request.method == 'POST':
        enseignant = Enseignant.objects.get(id=enseignant_id)
        enseignant.delete()
        messages.add_message(request, messages.SUCCESS, "L'enseignants a été supprimé avec succès", extra_tags='danger')
    return redirect('liste_enseignants')

"""salles"""
def liste_salles(request):
    salles = Salle.objects.all()
    return render(request, 'gestion_materiel/salles/liste_salles.html', {'salles': salles})

def liste_materiels_salle(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    materiels = Materiel.objects.filter(lieu=salle)
    return render(request, 'gestion_materiel/salles/liste_materiels_salle.html', {'salles': salle, 'materiels': materiels})

def ajout_salle(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salle ajoutée avec succès')
            return redirect('liste_salles')
    else:
        form = SalleForm()
    return render(request, 'gestion_materiel/salles/ajout_salle.html', {'form': form})

def supprimer_salle(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    salle.delete()
    messages.add_message(request, messages.SUCCESS, "La salles a été supprimée avec succès", extra_tags='danger')
    return redirect('liste_salles')


"""materiel"""
def liste_materiels(request):
    materiels = Materiel.objects.all()
    return render(request, 'gestion_materiel/materiel/liste_materiels.html', {'materiels': materiels})

def supprimer_materiel(request, materiel_id):
    materiel = get_object_or_404(Materiel, id=materiel_id)
    materiel.delete()
    messages.add_message(request, messages.SUCCESS, "Le matériel a été supprimé avec succès", extra_tags='danger')
    return redirect('liste_materiels')

def ajout_materiel(request):
    if request.method == 'POST':
        materiel_form = MaterielForm(request.POST)
        accessoire_formset = AccessoireFormSet(request.POST, prefix='accessoires')
        if materiel_form.is_valid() and accessoire_formset.is_valid():
            materiel = materiel_form.save()
            salle, created = Salle.objects.get_or_create(nom="001", etage="rez-de-chaussée")
            materiel.lieu = salle
            materiel.save()
            for form in accessoire_formset:
                if form.is_valid() and form.cleaned_data.get('nom'):
                    accessoire = form.save(commit=False)
                    accessoire.material = materiel
                    accessoire.save()
            messages.success(request, 'Matériel ajouté avec succès')
            return redirect('liste_materiels')
    else:
        materiel_form = MaterielForm()
        accessoire_formset = AccessoireFormSet(prefix='accessoires')

    return render(request, 'gestion_materiel/materiel/ajout_materiel.html',
                  {'materiel_form': materiel_form, 'accessoire_formset': accessoire_formset})


"""accessoire"""
def liste_accessoires(request, materiel_id):
    materiel = Materiel.objects.get(id=materiel_id)
    accessoires = AccessoireMateriel.objects.filter(material=materiel)
    return render(request, 'gestion_materiel/materiel/accessoire/liste_accessoires.html', {'materiel': materiel, 'accessoires': accessoires})

def supprimer_accessoire(request, materiel_id, accessoire_id):
    accessoire = get_object_or_404(AccessoireMateriel, id=accessoire_id)
    accessoire.delete()
    messages.add_message(request, messages.SUCCESS, "L'accessoire a été supprimé avec succès", extra_tags='danger')
    return redirect('liste_accessoires', materiel_id=materiel_id)

def modifier_accessoire(request, materiel_id, accessoire_id):
    accessoire = get_object_or_404(AccessoireMateriel, id=accessoire_id)
    materiel = Materiel.objects.get(id=materiel_id)
    if request.method == 'POST':
        form = AccessoireViaMaterielForm(request.POST, instance=accessoire)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accessoire modifié avec succès')
            return redirect('liste_accessoires', materiel_id=materiel_id)
    else:
        form = AccessoireViaMaterielForm(instance=accessoire)

    return render(request, 'gestion_materiel/materiel/accessoire/modifier_accessoire.html', {'form': form, 'materiel': materiel})

def ajouter_accessoire_via_materiel(request, materiel_id):
    materiel = get_object_or_404(Materiel, id=materiel_id)

    if request.method == 'POST':
        form = AccessoireViaMaterielForm(request.POST)
        if form.is_valid():
            accessoire = form.save(commit=False)
            accessoire.material = materiel
            accessoire.save()
            messages.success(request, 'Accessoire ajouté avec succès')
            return redirect('liste_accessoires', materiel_id=materiel.id)
    else:
        form = AccessoireViaMaterielForm()

    return render(request, 'gestion_materiel/materiel/accessoire/ajout_accessoire_via_materiel.html', {'materiel': materiel, 'form': form})

"""transfert"""
from django.shortcuts import render, redirect
from gestion_materiel.models import Materiel

def choix_materiel(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'historique':
            materiel_id = request.POST.get('materiel', '')
            return redirect('liste_historique_transferts', materiel_id=materiel_id)
        elif action == 'creation':
            materiel_id = request.POST.get('materiel', '')
            return redirect('ajout_transfert', materiel_id=materiel_id)

    materiels = Materiel.objects.all()
    selected_materiel_id = request.session.get('selected_materiel_id', None)

    return render(request, 'gestion_materiel/transfert/choix_materiel.html', {
        'materiels': materiels,
        'selected_materiel_id': selected_materiel_id,
    })

def ajout_transfert(request, materiel_id):
    materiel = Materiel.objects.get(id=materiel_id)
    accessoires = materiel.accessoiremateriel_set.all()

    enseignants = Enseignant.objects.all()
    salles = Salle.objects.all()

    if request.method == 'POST':
        form = TransfertForm(request.POST)
        if form.is_valid():

            transfert = form.save(commit=False)
            transfert.material = materiel
            transfert.ancien_possesseur = materiel.possesseur
            transfert.ancien_lieu = materiel.lieu

            salle_id = form.cleaned_data['nouveau_lieu'].id
            salle = Salle.objects.get(id=salle_id)

            if request.POST.get('rendre') == 'Oui':
                materiel.possesseur = None
                transfert.nouveau_possesseur = None
                materiel.lieu = Salle.objects.get(nom="001", etage="rez-de-chaussée")
            else:
                materiel.possesseur = transfert.nouveau_possesseur
                materiel.lieu = salle

            materiel.save()
            transfert.save()

            for accessoire in accessoires:
                present_key = 'present_' + str(accessoire.id)
                etat_key = 'etat_' + str(accessoire.id)

                present_value = request.POST.get(present_key)
                if present_value == "Oui":
                    nouvelle_presence = True
                    nouvel_etat = request.POST.get(etat_key, accessoire.etat)
                else:
                    nouvelle_presence = False
                    nouvel_etat = "Absent"

                TransfertAccessoire.objects.create(
                    transfert=transfert,
                    accessoire=accessoire,
                    ancienne_presence=accessoire.present,
                    nouvelle_presence=nouvelle_presence,
                    ancien_etat=accessoire.etat,
                    nouveau_etat=nouvel_etat
                )

                accessoire.present = nouvelle_presence
                accessoire.etat = nouvel_etat
                accessoire.save()

            return redirect('afficher_transfert', materiel_id=materiel.id, transfert_id=transfert.id)
    else:
        initial_data = {
            'material': materiel,
            'ancien_possesseur': materiel.possesseur,
            'ancien_lieu': materiel.lieu,
        }
        form = TransfertForm(initial=initial_data)

    return render(request, 'gestion_materiel/transfert/ajout_transfert.html', {
        'form': form,
        'materiel': materiel,
        'accessoires': accessoires,
        'enseignants': enseignants,
        'salles': salles,
    })

def liste_historique_transferts(request, materiel_id):
    materiel = get_object_or_404(Materiel, id=materiel_id)
    transferts = TransfertMateriel.objects.filter(material=materiel).order_by('-date_transfert')

    return render(request, 'gestion_materiel/transfert/liste_historique_transferts.html', {
        'materiel': materiel,
        'transferts': transferts,
    })

def afficher_transfert(request, materiel_id, transfert_id):
    materiel = Materiel.objects.get(id=materiel_id)
    transfert = TransfertMateriel.objects.get(id=transfert_id)
    salle_transfer = transfert.nouveau_lieu

    return render(request, 'gestion_materiel/transfert/afficher_transfert.html', {
        'materiel': materiel,
        'transfert': transfert,
        'salle_transfer': salle_transfer,
    })

def supprimer_transfert(request, materiel_id, transfert_id):
    transfert = get_object_or_404(TransfertMateriel, id=transfert_id)
    transfert.delete()
    messages.add_message(request, messages.SUCCESS, "Le transfert a été supprimé avec succès", extra_tags='danger')
    return redirect('liste_historique_transferts', materiel_id=materiel_id)