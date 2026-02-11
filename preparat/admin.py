from django.contrib import admin
from .models import (
    BiljniDodatak,
    BiljnaDroga,
    AktivnaSupstanca,
    Studija,
)


class BiljnaDrogaInline(admin.TabularInline):
    model = BiljnaDroga
    extra = 1


class AktivnaSupstancaInline(admin.TabularInline):
    model = AktivnaSupstanca
    extra = 1


class StudijaInline(admin.TabularInline):
    model = Studija
    extra = 1


@admin.register(BiljniDodatak)
class BiljniDodatakAdmin(admin.ModelAdmin):
    list_display = ("naziv", "oblik", "namena", "nacin_uzimanja")
    inlines = [BiljnaDrogaInline, AktivnaSupstancaInline, StudijaInline]


admin.site.register(BiljnaDroga)
admin.site.register(AktivnaSupstanca)
admin.site.register(Studija)
