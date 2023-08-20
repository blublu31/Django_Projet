from django import forms

from .models import Enseignant, Salle, AccessoireMateriel, Materiel, TransfertMateriel


class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['nom', 'prenom']

class SalleForm(forms.ModelForm):
    ETAGE_CHOICES = (
        ('rez-de-chaussee', 'Rez-de-chaussée'),
        ('1er', '1er étage'),
        ('2e', '2ème étage'),
        ('3e', '3ème étage'),

    )

    etage = forms.ChoiceField(choices=ETAGE_CHOICES)

    class Meta:
        model = Salle
        fields = ['nom', 'etage']

# forms.py
class AccessoireViaMaterielForm(forms.ModelForm):
    class Meta:
        model = AccessoireMateriel
        fields = ('nom', 'present', 'etat')
        widgets = {
            'etat': forms.Select(choices=[('Fonctionnel', 'Fonctionnel'), ('Défaillant', 'Défaillant'), ('Non fonctionnel', 'Non fonctionnel')]),
        }

    def clean_etat(self):
        if not self.cleaned_data['present']:
            return 'Absent'
        return self.cleaned_data['etat']

    def clean_nom(self):
        nom_accessoire = self.cleaned_data.get('nom')
        if not nom_accessoire:
            return None
        return nom_accessoire

class MaterielForm(forms.ModelForm):
    class Meta:
        model = Materiel
        fields = ('nom', 'budget', 'proprietaire')

AccessoireFormSet = forms.inlineformset_factory(
    Materiel,
    AccessoireMateriel,
    form=AccessoireViaMaterielForm,
    extra=2,
)

class TransfertForm(forms.ModelForm):
    class Meta:
        model = TransfertMateriel
        fields = ('nouveau_possesseur', 'date_transfert', 'nouveau_lieu', 'occasion', 'objectif')
        widgets = {
            'nouveau_possesseur': forms.Select(attrs={'class': 'form-control'}),
            'date_transfert': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'occasion': forms.TextInput(attrs={'class': 'form-control'}),
            'objectif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    nouveau_lieu = forms.ModelChoiceField(
        queryset=Salle.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nouveau_possesseur'].queryset = Enseignant.objects.all()
        self.fields['nouveau_lieu'].queryset = Salle.objects.all()
