from django import forms
from django.forms import inlineformset_factory
from .models import BiljniDodatak, BiljnaDroga, AktivnaSupstanca, Studija

# ===============================
# BILJNI DODATAK
# ===============================

class BiljniDodatakForm(forms.ModelForm):
    # Toggle polja
    ogranicenja_toggle = forms.BooleanField(required=False, label="Postoje ograničenja upotrebe")
    mjere_toggle = forms.BooleanField(required=False, label="Mjere opreza")
    upozorenja_toggle = forms.BooleanField(required=False, label="Upozorenja")

    # Polja unutar toggle sekcija
    ogranicenja_djeca = forms.BooleanField(required=False, label="Djeca")
    ogranicenja_trudnice = forms.BooleanField(required=False, label="Trudnice")
    ogranicenja_dojilje = forms.BooleanField(required=False, label="Dojilje")
    ogranicenja_hronicni = forms.BooleanField(required=False, label="Hronični")

    mjera_djeca = forms.BooleanField(required=False, label="Čuvati van domašaja djece")
    mjera_doziranje = forms.BooleanField(required=False, label="Ne prekoračiti preporučenu dnevnu dozu")
    mjera_zamjena = forms.BooleanField(required=False, label="Dodatak prehrani nije zamjena za ishranu")
    mjera_obrok = forms.BooleanField(required=False, label="Preporučuje se upotreba uz obrok")
    mjera_skladistenje = forms.BooleanField(required=False, label="Čuvati na suvom i tamnom mjestu")

    upozorenje_alergije = forms.BooleanField(required=False, label="Proizvod može izazvati alergijske reakcije")
    upozorenje_lijekovi = forms.BooleanField(required=False, label="Moguća interakcija sa lijekovima")
    upozorenje_gi = forms.BooleanField(required=False, label="Može izazvati gastrointestinalne smetnje")
    upozorenje_pritisak = forms.BooleanField(required=False, label="Može uticati na krvni pritisak")
    upozorenje_secer = forms.BooleanField(required=False, label="Može uticati na nivo šećera u krvi")

    # BSE / TSE
    bse_toggle = forms.BooleanField(required=False, label="Priloženo (BSE/TSE / GMO)")
    bse_napomena = forms.CharField(required=False, label="Napomena / naziv dokumenta",
                                   widget=forms.TextInput(attrs={"placeholder": "Unesite naziv dokumenta ili komentar"}))

    # Studije
    studije_toggle = forms.BooleanField(required=False, label="Postoje dokumenti")

    class Meta:
        model = BiljniDodatak
        fields = "__all__"
        widgets = {
            "naziv": forms.TextInput(attrs={"class": "input"}),
            "neto_kolicina": forms.NumberInput(attrs={"step": "any"}),
            "temp_min": forms.NumberInput(attrs={"step": "1"}),
            "temp_max": forms.NumberInput(attrs={"step": "1"}),
            "doza": forms.NumberInput(attrs={"step": "any"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # LOGIKA TOGGLE POLJA
        toggles = {
            "ogranicenja_toggle": ["ogranicenja_djeca", "ogranicenja_trudnice", "ogranicenja_dojilje", "ogranicenja_hronicni"],
            "mjere_toggle": ["mjera_djeca", "mjera_doziranje", "mjera_zamjena", "mjera_obrok", "mjera_skladistenje"],
            "upozorenja_toggle": ["upozorenje_alergije", "upozorenje_lijekovi", "upozorenje_gi", "upozorenje_pritisak", "upozorenje_secer"],
        }

        for toggle, fields in toggles.items():
            if not cleaned_data.get(toggle):
                for f in fields:
                    cleaned_data[f] = False

        if not cleaned_data.get("bse_toggle"):
            cleaned_data["bse_status"] = "nije_potrebno"
            cleaned_data["bse_napomena"] = ""

        # PROVJERA DUPLIKATA
        naziv = cleaned_data.get("naziv")
        oblik = cleaned_data.get("oblik")
        neto_kolicina = cleaned_data.get("neto_kolicina")
        jedinica_kolicina = cleaned_data.get("jedinica_kolicina")

        if naziv and oblik and neto_kolicina and jedinica_kolicina:
            if BiljniDodatak.objects.filter(
                naziv=naziv,
                oblik=oblik,
                neto_kolicina=neto_kolicina,
                jedinica_kolicina=jedinica_kolicina
            ).exists():
                self.instance.exists_in_db = True
            else:
                self.instance.exists_in_db = False

        return cleaned_data


# ===============================
# BILJNA DROGA
# ===============================

class BiljnaDrogaForm(forms.ModelForm):
    standardizacija_supstanca = forms.ModelChoiceField(
        queryset=AktivnaSupstanca.objects.none(),
        required=False,
        label="Standardizovano na supstancu"
    )

    class Meta:
        model = BiljnaDroga
        exclude = ("dodatak",)
        widgets = {
            "der": forms.TextInput(attrs={"placeholder": "npr. 5:1"}),
            "standardizacija_proc": forms.NumberInput(attrs={"step": "any"}),
            "kolicina_biljna": forms.NumberInput(attrs={"step": "any"}),
        }

    def __init__(self, *args, **kwargs):
        dodatak = kwargs.pop("dodatak", None)
        super().__init__(*args, **kwargs)
        if dodatak:
            self.fields["standardizacija_supstanca"].queryset = AktivnaSupstanca.objects.filter(dodatak=dodatak)
        else:
            self.fields["standardizacija_supstanca"].queryset = AktivnaSupstanca.objects.all()


# ===============================
# AKTIVNA SUPSTANCA
# ===============================

class AktivnaSupstancaForm(forms.ModelForm):
    class Meta:
        model = AktivnaSupstanca
        exclude = ("dodatak",)
        widgets = {"kolicina": forms.NumberInput(attrs={"step": "any"})}


# ===============================
# STUDIJA
# ===============================

class StudijaForm(forms.ModelForm):
    class Meta:
        model = Studija
        exclude = ("dodatak",)
        widgets = {
            "naziv": forms.TextInput(attrs={"placeholder": "npr. Studija etnofarmakologije"}),
            "tip": forms.Select(),
            "godina": forms.TextInput(attrs={"placeholder": "npr. 2021, Journal of Ethnopharmacology"}),
            "doi": forms.TextInput(attrs={"placeholder": "npr. 10.1016/j.jep.2021.114321"}),
        }


# ===============================
# FORMSETOVI
# ===============================

BiljnaDrogaFormSet = inlineformset_factory(BiljniDodatak, BiljnaDroga, form=BiljnaDrogaForm, extra=1, can_delete=True)
AktivnaSupstancaFormSet = inlineformset_factory(BiljniDodatak, AktivnaSupstanca, form=AktivnaSupstancaForm, extra=1, can_delete=True)
StudijaFormSet = inlineformset_factory(BiljniDodatak, Studija, form=StudijaForm, extra=1, can_delete=True)
