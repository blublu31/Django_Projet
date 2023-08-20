from django.contrib import admin
from .models import Enseignant, Salle, Materiel, TransfertMateriel, AccessoireMateriel, TransfertAccessoire


class EnseignantAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom")

class AccessoireMaterielAdmin(admin.ModelAdmin):
    list_display = ('nom', 'get_materiel_name', 'present', 'etat')

    def get_materiel_name(self, obj):
        return obj.material.nom if obj.material else "Aucun matériel"
    get_materiel_name.short_description = 'Matériel'

admin.site.register(Enseignant, EnseignantAdmin)
admin.site.register(Salle)
admin.site.register(Materiel)
admin.site.register(TransfertMateriel)
admin.site.register(AccessoireMateriel, AccessoireMaterielAdmin)
admin.site.register(TransfertAccessoire)