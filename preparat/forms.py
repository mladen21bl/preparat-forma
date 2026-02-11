from django import forms
from django.forms import inlineformset_factory
from .models import BiljniDodatak, BiljnaDroga, AktivnaSupstanca, Studija


class BiljniDodatakForm(forms.ModelForm):
    # Sekcija 4: Ograničenja i upozorenja
    ogranicenja_toggle = forms.BooleanField(required=False, label="Postoje ograničenja upotrebe")
    mjere_toggle = forms.BooleanField(required=False, label="Mjere opreza")
    upozorenja_toggle = forms.BooleanField(required=False, label="Upozorenja")

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

    # BSE/TSE
    bse_toggle = forms.BooleanField(
    required=False, 
    label="Priloženo (BSE/TSE / GMO)",
    help_text="Označite ako su sertifikati priloženi.")
    bse_napomena = forms.CharField(
    required=False, 
    label="Napomena / naziv dokumenta",
    widget=forms.TextInput(attrs={"placeholder": "Unesite naziv dokumenta ili komentar"}))


    # Klinicke studije toggle (formset i dalje kroz StudijaFormSet)
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
            "bse_napomena": forms.TextInput(),
        }


class BiljnaDrogaForm(forms.ModelForm):
    class Meta:
        model = BiljnaDroga
        exclude = ("dodatak",)
        widgets = {
            "der": forms.TextInput(attrs={"placeholder": "npr. 5:1"}),
            "standardizacija_proc": forms.NumberInput(attrs={"step": "any"}),
            "kolicina_biljna": forms.NumberInput(attrs={"step": "any"}),
            "standardizacija_supstanca": forms.Select(),  # dropdown
        }


class AktivnaSupstancaForm(forms.ModelForm):
    class Meta:
        model = AktivnaSupstanca
        exclude = ("dodatak",)
        widgets = {
            "kolicina": forms.NumberInput(attrs={"step": "any"}),
        }


class StudijaForm(forms.ModelForm):
    class Meta:
        model = Studija
        exclude = ("dodatak",)
        widgets = {
            "naziv": forms.TextInput(attrs={"placeholder": "npr. Studija etnofarmakologije"}),
            "tip": forms.Select(attrs={"placeholder": "Odaberite tip studije"}),
            "godina": forms.TextInput(attrs={"placeholder": "npr. 2021, Journal of Ethnopharmacology"}),
            "doi": forms.TextInput(attrs={"placeholder": "npr. 10.1016/j.jep.2021.114321"}),
        }
        help_texts = {
            "tip": "Kliničko: studije na ljudima.\nLaboratorijsko / pre-kliničko: studije in vitro ili na životinjama.\nLiteratura / review: pregledni radovi i meta-analize.",
            "doi": "DOI (Digital Object Identifier) je jedinstveni identifikator naučne publikacije."
        }


BiljnaDrogaFormSet = inlineformset_factory(
    BiljniDodatak,
    BiljnaDroga,
    form=BiljnaDrogaForm,
    extra=1,
    can_delete=True,
)


AktivnaSupstancaFormSet = inlineformset_factory(
    BiljniDodatak,
    AktivnaSupstanca,
    form=AktivnaSupstancaForm,
    extra=1,
    can_delete=True,
)


StudijaFormSet = inlineformset_factory(
    BiljniDodatak,
    Studija,
    form=StudijaForm,
    extra=1,
    can_delete=True,
)
