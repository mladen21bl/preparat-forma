# models.py
from django.db import models


class BiljniDodatak(models.Model):

    # ====== CHOICES ======

    OBLIK_CHOICES = [
        ("tablete", "Tablete"),
        ("kapsule", "Kapsule"),
        ("prah", "Prah"),
        ("granule", "Granule"),
        ("pastile", "Pastile"),
        ("mast", "Mast"),
        ("gel", "Gel"),
        ("krem", "Krem"),
        ("sirup", "Sirup"),
        ("oralni_rastvor", "Oralni rastvor"),
        ("kapi", "Kapi"),
        ("tinktura", "Tinktura"),
        ("sprej", "Sprej"),
        ("ulje", "Ulje"),
        ("caj", "Čaj"),
    ]

    JEDINICA_KOLICINA_CHOICES = [
        ("g", "g"),
        ("mg", "mg"),
        ("ml", "ml"),
        ("µg", "µg"),
        ("kapsula", "kapsula"),
        ("tableta", "tableta"),
        ("vrecica", "vrećica"),
    ]

    TIP_AMBALAZE_CHOICES = [
        ("bocica", "Bočica"),
        ("blister", "Blister"),
        ("vrecica", "Vrećica"),
        ("pakiranje_caj", "Pakovanje za čaj"),
        ("tubica", "Tubica"),
        ("teglica", "Teglica"),
        ("kartonska_kutija", "Kartonska kutija"),
        ("bocica_kapaljka", "Bočica sa kapaljkom"),
    ]

    MATERIJAL_AMBALAZE_CHOICES = [
        ("plastika", "Plastika"),
        ("staklo", "Staklo"),
        ("aluminij", "Aluminijum"),
        ("papir", "Papir / Karton"),
        ("metal", "Metal"),
    ]

    NAMENA_CHOICES = [
        ("poboljsava_imunitet", "Poboljšava imunitet"),
        ("poboljsava_probavu", "Poboljšava probavu"),
        ("zdravlje_kose_koze", "Zdravlje kose / kože / noktiju"),
        ("poboljsava_kosti", "Poboljšava zdravlje kostiju"),
        ("smanjuje_umor", "Smanjuje umor"),
        ("poboljsava_cirkulaciju", "Poboljšava cirkulaciju"),
        ("podrzava_jetru", "Podrška funkciji jetre"),
        ("poboljsava_snovi", "Poboljšava san"),
        ("opste_zdravlje", "Opšte zdravlje"),
        ("poboljsava_imunitet_probavu", "Imunitet + probava"),
    ]

    JEDINICA_DOZA_CHOICES = [
        ("kapsula", "Kapsula"),
        ("tableta", "Tableta"),
        ("ml", "ml"),
        ("kasika", "Kašika"),
        ("kasicica", "Kašičica"),
        ("vrecica", "Vrećica"),
    ]

    NACIN_UZIMANJA_CHOICES = [
        ("oralno", "Oralno"),
        ("sublingvalno", "Sublingvalno"),
        ("lokalno", "Lokalno"),
        ("inhalacija", "Inhalacija"),
    ]

    BSE_STATUS_CHOICES = [
        ("nije_potrebno", "Nije potrebno"),
        ("prilozeno", "Priloženo"),
    ]

    # ====== POLJA ======

    naziv = models.CharField(max_length=255)

    oblik = models.CharField(max_length=50, choices=OBLIK_CHOICES)
    neto_kolicina = models.FloatField(null=True, blank=True)
    jedinica_kolicina = models.CharField(max_length=20, choices=JEDINICA_KOLICINA_CHOICES, null=True, blank=True)

    tip_ambalaze = models.CharField(max_length=50, choices=TIP_AMBALAZE_CHOICES)
    materijal_ambalaze = models.CharField(max_length=50, choices=MATERIJAL_AMBALAZE_CHOICES)

    zastita_svjetlost = models.BooleanField(default=False)
    zastita_vlaga = models.BooleanField(default=False)

    temp_min = models.IntegerField(null=True, blank=True)
    temp_max = models.IntegerField(null=True, blank=True)

    namena = models.CharField(max_length=100, choices=NAMENA_CHOICES)
    doza = models.FloatField(null=True, blank=True)
    jedinica_doza = models.CharField(max_length=20, choices=JEDINICA_DOZA_CHOICES, null=True, blank=True)

    nacin_uzimanja = models.CharField(max_length=50, choices=NACIN_UZIMANJA_CHOICES)

    ogranicenja_djeca = models.BooleanField(default=False)
    ogranicenja_trudnice = models.BooleanField(default=False)
    ogranicenja_dojilje = models.BooleanField(default=False)
    ogranicenja_hronicni = models.BooleanField(default=False)

    mjera_djeca = models.BooleanField(default=False)
    mjera_doziranje = models.BooleanField(default=False)
    mjera_zamjena = models.BooleanField(default=False)
    mjera_obrok = models.BooleanField(default=False)
    mjera_skladistenje = models.BooleanField(default=False)

    upozorenje_alergije = models.BooleanField(default=False)
    upozorenje_lijekovi = models.BooleanField(default=False)
    upozorenje_gi = models.BooleanField(default=False)
    upozorenje_pritisak = models.BooleanField(default=False)
    upozorenje_secer = models.BooleanField(default=False)

    bse_status = models.CharField(max_length=20, choices=BSE_STATUS_CHOICES, default="nije_potrebno")
    bse_napomena = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.naziv


class BiljnaDroga(models.Model):

    DIO_BILJKE_CHOICES = [
        ("korijen", "Korijen"),
        ("rizom", "Rizom"),
        ("list", "List"),
        ("cvijet", "Cvijet"),
        ("plod", "Plod"),
        ("sjeme", "Sjeme"),
        ("kora", "Kora"),
        ("herba", "Herba"),
    ]

    STANJE_BILJKE_CHOICES = [
        ("svjeza", "Svježa"),
        ("osusena", "Osušena"),
        ("fermentisana", "Fermentisana"),
        ("preradjena", "Prerađena / ekstrakt"),
        ("prah", "Prah"),
    ]

    RASTVARAC_CHOICES = [
        ("voda", "Voda"),
        ("etanol_70", "70% Etanol"),
        ("metanol", "Metanol"),
        ("aceton", "Aceton"),
        ("glicerol", "Glicerol"),
        ("propilen_glikol", "Propilen glikol"),
    ]

    JEDINICA_BILJNA_CHOICES = [
        ("mg", "mg"),
        ("g", "g"),
        ("ml", "ml"),
        ("%", "%"),
    ]

    ZEMLJA_CHOICES = [
        ("srbija", "Srbija"),
        ("bih", "Bosna i Hercegovina"),
        ("eu", "EU"),
    ]

    dodatak = models.ForeignKey(BiljniDodatak, on_delete=models.CASCADE, related_name="biljne_droge")

    biljka_sr = models.CharField(max_length=255)
    biljka_lat = models.CharField(max_length=255)

    dio_biljke = models.CharField(max_length=50, choices=DIO_BILJKE_CHOICES)
    stanje_biljke = models.CharField(max_length=50, choices=STANJE_BILJKE_CHOICES)
    rastvarac = models.CharField(max_length=50, choices=RASTVARAC_CHOICES)

    der = models.CharField(max_length=50, blank=True)

    standardizacija_proc = models.FloatField(null=True, blank=True)
    standardizacija_supstanca = models.CharField(max_length=100, blank=True)

    zemlja_porijekla = models.CharField(max_length=50, choices=ZEMLJA_CHOICES, blank=True)

    kolicina_biljna = models.FloatField(null=True, blank=True)
    jedinica_biljna = models.CharField(max_length=20, choices=JEDINICA_BILJNA_CHOICES, blank=True)

    def __str__(self):
        return f"{self.biljka_sr} ({self.biljka_lat})"


class AktivnaSupstanca(models.Model):

    PORIJEKLO_CHOICES = [
        ("biljna", "Iz biljne droge"),
        ("sintetska", "Sintetska"),
        ("mineralna", "Mineralna"),
        ("animalna", "Animalna"),
    ]

    JEDINICA_CHOICES = [
        ("mg", "mg"),
        ("µg", "µg"),
        ("g", "g"),
        ("ml", "ml"),
        ("IU", "IU"),
    ]

    dodatak = models.ForeignKey(BiljniDodatak, on_delete=models.CASCADE, related_name="aktivne_supstance")

    naziv = models.CharField(max_length=255)
    hemijski_oblik = models.CharField(max_length=255, blank=True)

    kolicina = models.FloatField(null=True, blank=True)
    jedinica = models.CharField(max_length=20, choices=JEDINICA_CHOICES, blank=True)

    porijeklo = models.CharField(max_length=50, choices=PORIJEKLO_CHOICES)

    def __str__(self):
        return self.naziv


class Studija(models.Model):

    TIP_CHOICES = [
        ("klinicko", "Kliničko"),
        ("laboratorijsko", "Laboratorijsko / pre-kliničko"),
        ("literatura", "Literatura / review"),
    ]

    dodatak = models.ForeignKey(BiljniDodatak, on_delete=models.CASCADE, related_name="studije")

    naziv = models.CharField(max_length=255)
    tip = models.CharField(max_length=50, choices=TIP_CHOICES)
    godina = models.CharField(max_length=100, blank=True)
    doi = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.naziv

