from django.shortcuts import render, redirect
from math import isclose
from .models import BiljniDodatak, BiljnaDroga, AktivnaSupstanca, Studija


# =========================
# Osnovne stranice
# =========================

def index(request):
    return render(request, "preparat/index.html")


def success_view(request):
    return render(request, "preparat/success.html")


# =========================
# GLAVNI EVALUACIONI VIEW
# =========================


from django.shortcuts import render, redirect, get_object_or_404
from math import isclose
from .models import BiljniDodatak


from math import isclose
from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, redirect, get_object_or_404
from .models import BiljniDodatak, BiljnaDroga, AktivnaSupstanca, Studija
from math import isclose

def prijava_test2(request):
    # Pretpostavljamo da postoji samo jedna instanca u bazi
    dodatak = BiljniDodatak.objects.first()
    supstance = AktivnaSupstanca.objects.filter(dodatak=dodatak)

    greske = {}  # ovde ćemo beležiti koja polja su pogrešna

    if request.method == "POST":
        data = request.POST

        # --- 1. Osnovni podaci ---
        if data.get("naziv") != dodatak.naziv:
            greske["naziv"] = True
        if data.get("oblik") != dodatak.oblik:
            greske["oblik"] = True
        try:
            if not isclose(float(data.get("neto_kolicina", 0)), float(dodatak.neto_kolicina or 0)):
                greske["neto_kolicina"] = True
        except:
            greske["neto_kolicina"] = True
        if data.get("jedinica_kolicina") != dodatak.jedinica_kolicina:
            greske["jedinica_kolicina"] = True

        # --- 2. Ambalaža ---
        if data.get("tip_ambalaze") != dodatak.tip_ambalaze:
            greske["tip_ambalaze"] = True
        if data.get("materijal_ambalaze") != dodatak.materijal_ambalaze:
            greske["materijal_ambalaze"] = True
        try:
            if int(data.get("temp_min", 0)) != (dodatak.temp_min or 0):
                greske["temp_min"] = True
        except:
            greske["temp_min"] = True
        try:
            if int(data.get("temp_max", 0)) != (dodatak.temp_max or 0):
                greske["temp_max"] = True
        except:
            greske["temp_max"] = True

        # --- 3. Namena i doza ---
        if data.get("namena") != dodatak.namena:
            greske["namena"] = True
        try:
            if not isclose(float(data.get("doza", 0)), float(dodatak.doza or 0)):
                greske["doza"] = True
        except:
            greske["doza"] = True
        if data.get("jedinica_doza") != dodatak.jedinica_doza:
            greske["jedinica_doza"] = True
        if data.get("nacin_uzimanja") != dodatak.nacin_uzimanja:
            greske["nacin_uzimanja"] = True

        # --- 4. Checkboxovi (ograničenja i upozorenja) ---
        checkbox_polja = [
            "ogranicenja_djeca", "ogranicenja_trudnice", "ogranicenja_dojilje", "ogranicenja_hronicni",
            "mjera_djeca", "mjera_doziranje", "mjera_zamjena", "mjera_obrok", "mjera_skladistenje",
            "upozorenje_alergije", "upozorenje_lijekovi", "upozorenje_gi", "upozorenje_pritisak", "upozorenje_secer"
        ]
        for polje in checkbox_polja:
            vrednost_forme = polje in data
            vrednost_baze = getattr(dodatak, polje)
            if vrednost_forme != vrednost_baze:
                greske[polje] = True

        # --- 5. BSE ---
        if data.get("bse_status") != dodatak.bse_status:
            greske["bse_status"] = True
        if data.get("bse_napomena", "").strip() != (dodatak.bse_napomena or "").strip():
            greske["bse_napomena"] = True

        # --- 6. Biljna droga ---
        biljke_sr = data.getlist("biljka_sr[]")
        biljke_lat = data.getlist("biljka_lat[]")
        dio_biljke = data.getlist("dio_biljke[]")
        stanje_biljke = data.getlist("stanje_biljke[]")
        rastvarac = data.getlist("rastvarac[]")
        der = data.getlist("der[]")
        standardizacija_proc = data.getlist("standardizacija_proc[]")
        standardizacija_supstanca = data.getlist("standardizacija_supstanca[]")
        zemlja_porijekla = data.getlist("zemlja_porijekla[]")
        kolicina_biljna = data.getlist("kolicina_biljna[]")
        jedinica_biljna = data.getlist("jedinica_biljna[]")

        droge_baza = list(dodatak.biljne_droge.all())

        if len(biljke_sr) != len(droge_baza):
            greske["biljna_droga"] = True
        else:
            for i, droga in enumerate(droge_baza):
                if biljke_sr[i] != droga.biljka_sr:
                    greske[f"biljka_sr_{i}"] = True
                if biljke_lat[i] != droga.biljka_lat:
                    greske[f"biljka_lat_{i}"] = True
                if dio_biljke[i] != droga.dio_biljke:
                    greske[f"dio_biljke_{i}"] = True
                if stanje_biljke[i] != droga.stanje_biljke:
                    greske[f"stanje_biljke_{i}"] = True
                if rastvarac[i] != droga.rastvarac:
                    greske[f"rastvarac_{i}"] = True
                if der[i] != (droga.der or ""):
                    greske[f"der_{i}"] = True
                try:
                    if standardizacija_proc[i] and not isclose(float(standardizacija_proc[i]), float(droga.standardizacija_proc or 0)):
                        greske[f"standardizacija_proc_{i}"] = True
                except:
                    greske[f"standardizacija_proc_{i}"] = True
                if standardizacija_supstanca[i]:
                    if int(standardizacija_supstanca[i]) != (droga.standardizacija_supstanca.id if droga.standardizacija_supstanca else None):
                        greske[f"standardizacija_supstanca_{i}"] = True
                if zemlja_porijekla[i] != (droga.zemlja_porijekla or ""):
                    greske[f"zemlja_porijekla_{i}"] = True
                try:
                    if kolicina_biljna[i] and not isclose(float(kolicina_biljna[i]), float(droga.kolicina_biljna or 0)):
                        greske[f"kolicina_biljna_{i}"] = True
                except:
                    greske[f"kolicina_biljna_{i}"] = True
                if jedinica_biljna[i] != (droga.jedinica_biljna or ""):
                    greske[f"jedinica_biljna_{i}"] = True

        # --- 7. Aktivne supstance ---
        aktivne_naziv = data.getlist("aktivna_naziv[]")
        hemijski_oblik = data.getlist("hemijski_oblik[]")
        kolicina_aktivna = data.getlist("kolicina_aktivna[]")
        jedinica_aktivna = data.getlist("jedinica_aktivna[]")

        aktivne_baza = list(dodatak.aktivne_supstance.all())

        if len(aktivne_naziv) != len(aktivne_baza):
            greske["aktivne_supstance"] = True
        else:
            for i, sup in enumerate(aktivne_baza):
                if aktivne_naziv[i] != sup.naziv:
                    greske[f"aktivna_naziv_{i}"] = True
                if hemijski_oblik[i] != (sup.hemijski_oblik or ""):
                    greske[f"hemijski_oblik_{i}"] = True
                try:
                    if kolicina_aktivna[i] and not isclose(float(kolicina_aktivna[i]), float(sup.kolicina or 0)):
                        greske[f"kolicina_aktivna_{i}"] = True
                except:
                    greske[f"kolicina_aktivna_{i}"] = True
                if jedinica_aktivna[i] != (sup.jedinica or ""):
                    greske[f"jedinica_aktivna_{i}"] = True

        # --- 8. Studije ---
        study_naziv = data.getlist("study_naziv[]")
        study_tip = data.getlist("study_tip[]")
        study_godina = data.getlist("study_godina[]")
        study_doi = data.getlist("study_doi[]")

        studije_baza = list(dodatak.studije.all())

        if len(study_naziv) != len(studije_baza):
            greske["studije"] = True
        else:
            for i, s in enumerate(studije_baza):
                if study_naziv[i] != s.naziv:
                    greske[f"study_naziv_{i}"] = True
                if study_tip[i] != s.tip:
                    greske[f"study_tip_{i}"] = True
                if (study_godina[i] or "").strip() != (s.godina or "").strip():
                    greske[f"study_godina_{i}"] = True
                if (study_doi[i] or "").strip() != (s.doi or "").strip():
                    greske[f"study_doi_{i}"] = True

        # --- Kraj evaluacije ---
        if not greske:
            return redirect("success")

    else:
        data = {}

    context = {
        "dodatak": dodatak,
        "supstance": supstance,
        "greske": greske,
        "data": data,
    }
    return render(request, "preparat/test.html", context)