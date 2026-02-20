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
from .models import BiljniDodatak


from django.shortcuts import render, get_object_or_404, redirect
from .models import BiljniDodatak


from django.shortcuts import render, get_object_or_404, redirect
from .models import BiljniDodatak

def prijava_test2(request):
    context = {}

    if request.method == "POST":
        naziv = request.POST.get("naziv", "").strip()

        # Referentni objekat iz baze
        dodatak = get_object_or_404(BiljniDodatak, naziv=naziv)

        greske = {}
        uneseno = request.POST.copy()

        # ===== POMOĆNE FUNKCIJE =====
        def check(field):
            db_val = getattr(dodatak, field) or ""
            post_val = uneseno.get(field) or ""
            if str(db_val).strip() != str(post_val).strip():
                greske[field] = True

        def check_float(field):
            db_val = getattr(dodatak, field)
            post_val = uneseno.get(field)

            if (db_val is None or db_val == "") and not post_val:
                return

            try:
                if float(db_val) != float(post_val):
                    greske[field] = True
            except:
                greske[field] = True

        # ===== 1. OSNOVNA POLJA =====
        osnovna_polja = [
            "naziv",
            "oblik",
            "jedinica_kolicina",
            "tip_ambalaze",
            "materijal_ambalaze",
            "namena",
            "jedinica_doza",
            "nacin_uzimanja",
            "bse_status",
        ]

        for f in osnovna_polja:
            check(f)

        for f in ["neto_kolicina", "doza", "temp_min", "temp_max"]:
            check_float(f)

        # ===== 2. BOOLEAN POLJA =====
        bool_polja = [
            "zastita_svjetlost",
            "zastita_vlaga",
            "ogranicenja_djeca",
            "ogranicenja_trudnice",
            "ogranicenja_dojilje",
            "ogranicenja_hronicni",
            "mjera_djeca",
            "mjera_doziranje",
            "mjera_zamjena",
            "mjera_obrok",
            "mjera_skladistenje",
            "upozorenje_alergije",
            "upozorenje_lijekovi",
            "upozorenje_gi",
            "upozorenje_pritisak",
            "upozorenje_secer",
        ]

        for f in bool_polja:
            db_val = getattr(dodatak, f) or False
            post_val = f in uneseno
            if db_val != post_val:
                greske[f] = True

        # ===== 3. BILJNE DROGE =====
        biljke_post = uneseno.getlist("biljka_sr[]")
        biljke_db = list(dodatak.biljne_droge.all())

        if len(biljke_post) != len(biljke_db):
            greske["biljne_droge"] = True
        else:
            for i, droga in enumerate(biljke_db):
                if (droga.biljka_sr or "").strip() != (biljke_post[i] or "").strip():
                    greske[f"biljka_sr_{i}"] = True

        # ===== 4. AKTIVNE SUPSTANCE =====
        aktivne_post = uneseno.getlist("aktivna_naziv[]")
        aktivne_db = list(dodatak.aktivne_supstance.all())

        if len(aktivne_post) != len(aktivne_db):
            greske["aktivne_supstance"] = True
        else:
            for i, sup in enumerate(aktivne_db):
                if (sup.naziv or "").strip() != (aktivne_post[i] or "").strip():
                    greske[f"aktivna_naziv_{i}"] = True

        # ===== 5. STUDIJE =====
        studije_post = uneseno.getlist("study_naziv[]")
        studije_db = list(dodatak.studije.all())

        if len(studije_post) != len(studije_db):
            greske["studije"] = True
        else:
            for i, s in enumerate(studije_db):
                if (s.naziv or "").strip() != (studije_post[i] or "").strip():
                    greske[f"study_naziv_{i}"] = True

        # ===== 6. BSE NAPOMENA =====
        if dodatak.bse_status == "prilozeno":
            if (uneseno.get("bse_napomena") or "").strip() != (dodatak.bse_napomena or "").strip():
                greske["bse_napomena"] = True

        # ===== REZULTAT =====
        if not greske:
            return redirect("success")  # ili gde već vodiš po uspešnom unosu

        context["greske"] = greske
        context["uneseno"] = uneseno

    return render(request, "preparat/test.html", context)
