from math import isclose
from .models import BiljniDodatak, BiljnaDroga, AktivnaSupstanca, Studija
from django.shortcuts import render, redirect, get_object_or_404

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




from math import isclose
from django.shortcuts import render, redirect
from .models import BiljniDodatak, AktivnaSupstanca

def prijava_test2(request):
    dodatak = BiljniDodatak.objects.first()
    supstance = AktivnaSupstanca.objects.filter(dodatak=dodatak)
    greske = {}
    data = request.POST if request.method == "POST" else {}

    if request.method == "POST":
        # --- 1. Osnovni podaci ---
        osnovna_polja = {
            "naziv": dodatak.naziv,
            "oblik": dodatak.oblik,
            "jedinica_kolicina": dodatak.jedinica_kolicina or "",
            "jedinica_doza": dodatak.jedinica_doza or "",
            "namena": dodatak.namena,
            "nacin_uzimanja": dodatak.nacin_uzimanja,
        }
        for polje, vrijednost in osnovna_polja.items():
            if data.get(polje) != vrijednost:
                greske[polje] = True

        # Polja koja su float
        float_polja = {
            "neto_kolicina": dodatak.neto_kolicina or 0,
            "doza": dodatak.doza or 0,
        }
        for polje, vrijednost in float_polja.items():
            try:
                if not isclose(float(data.get(polje, 0)), float(vrijednost)):
                    greske[polje] = True
            except:
                greske[polje] = True

        # Polja koja su int
        int_polja = {
            "temp_min": dodatak.temp_min or 0,
            "temp_max": dodatak.temp_max or 0,
        }
        for polje, vrijednost in int_polja.items():
            try:
                if int(data.get(polje, 0)) != vrijednost:
                    greske[polje] = True
            except:
                greske[polje] = True

        # --- 2. Checkboxovi ---
        checkbox_polja = [
            "ogranicenja_djeca","ogranicenja_trudnice","ogranicenja_dojilje","ogranicenja_hronicni",
            "mjera_djeca","mjera_doziranje","mjera_zamjena","mjera_obrok","mjera_skladistenje",
            "upozorenje_alergije","upozorenje_lijekovi","upozorenje_gi","upozorenje_pritisak","upozorenje_secer"
        ]
        for polje in checkbox_polja:
            if (polje in data) != getattr(dodatak, polje):
                greske[polje] = True

        # --- 3. BSE ---
        if data.get("bse_status") != dodatak.bse_status:
            greske["bse_status"] = True
        if (data.get("bse_napomena") or "").strip() != (dodatak.bse_napomena or "").strip():
            greske["bse_napomena"] = True

        # --- 4. Biljna droga ---
        droge_baza = list(dodatak.biljne_droge.all())
        biljke_sr = data.getlist("biljka_sr")
        if len(biljke_sr) != len(droge_baza):
            greske["biljna_droga"] = True
        else:
            for i, droga in enumerate(droge_baza):
                fields = [
                    ("biljka_sr", droga.biljka_sr),
                    ("biljka_lat", droga.biljka_lat),
                    ("dio_biljke", droga.dio_biljke),
                    ("stanje_biljke", droga.stanje_biljke),
                    ("rastvarac", droga.rastvarac),
                    ("der", droga.der or ""),
                    ("zemlja_porijekla", droga.zemlja_porijekla or ""),
                    ("jedinica_biljna", droga.jedinica_biljna or "")
                ]
                for polje, vrijednost in fields:
                    if data.getlist(polje)[i] != vrijednost:
                        greske[f"{polje}_{i}"] = True

                # Standardizacija proc
                try:
                    proc = data.getlist("standardizacija_proc")[i]
                    if proc and not isclose(float(proc), float(droga.standardizacija_proc or 0)):
                        greske[f"standardizacija_proc_{i}"] = True
                except:
                    if data.getlist("standardizacija_proc")[i]:
                        greske[f"standardizacija_proc_{i}"] = True

                # Standardizacija supstanca
                sup_id_str = data.getlist("standardizacija_supstanca")[i]
                sup_id = int(sup_id_str) if sup_id_str else None
                baza_id = droga.standardizacija_supstanca.id if droga.standardizacija_supstanca else None
                if sup_id != baza_id:
                    greske[f"standardizacija_supstanca_{i}"] = True

                # Kolicina biljna (float)
                try:
                    kol = data.getlist("kolicina_biljna")[i]
                    if kol and not isclose(float(kol), float(droga.kolicina_biljna or 0)):
                        greske[f"kolicina_biljna_{i}"] = True
                except:
                    greske[f"kolicina_biljna_{i}"] = True

        # --- 5. Aktivne supstance ---
        aktivne_baza = list(dodatak.aktivne_supstance.all())
        aktivne_naziv = data.getlist("aktivna_naziv")
        if len(aktivne_naziv) != len(aktivne_baza):
            greske["aktivne_supstance"] = True
        else:
            for i, sup in enumerate(aktivne_baza):
                fields = [
                    ("aktivna_naziv", sup.naziv),
                    ("hemijski_oblik", sup.hemijski_oblik or ""),
                    ("jedinica_aktivna", sup.jedinica or "")
                ]
                for polje, vrijednost in fields:
                    if data.getlist(polje)[i] != vrijednost:
                        greske[f"{polje}_{i}"] = True
                # Kolicina aktivna
                try:
                    kolicina = data.getlist("kolicina_aktivna")[i]
                    if kolicina and not isclose(float(kolicina), float(sup.kolicina or 0)):
                        greske[f"kolicina_aktivna_{i}"] = True
                except:
                    greske[f"kolicina_aktivna_{i}"] = True

        # --- 6. Studije ---
        studije_baza = list(dodatak.studije.all())
        study_naziv = data.getlist("study_naziv")
        if len(study_naziv) != len(studije_baza):
            greske["studije"] = True
        else:
            for i, s in enumerate(studije_baza):
                fields = [
                    ("study_naziv", s.naziv),
                    ("study_tip", s.tip),
                    ("study_godina", s.godina or ""),
                    ("study_doi", s.doi or "")
                ]
                for polje, vrijednost in fields:
                    if (data.getlist(polje)[i] or "").strip() != vrijednost.strip():
                        greske[f"{polje}_{i}"] = True

        # --- 7. Redirect ili render ---
        if not greske:
            return redirect("success")

    context = {
        "dodatak": dodatak,
        "supstance": supstance,
        "greske": greske,
        "data": data,
    }
    return render(request, "preparat/test.html", context)