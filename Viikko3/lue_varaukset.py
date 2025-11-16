"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funkitoita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,90 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime

def hae_varausnumero(varaus):
    numero = int(varaus[0])
    print(f"Varausnumero: {numero}")

def hae_varaaja(varaus):
    nimi = varaus[1]
    print(f"Varaaja: {nimi}")

def hae_paiva(varaus):
    # Luetaan muodossa 2025-10-31
    paiva = datetime.strptime(varaus[2], "%Y-%m-%d")
    # Tulostetaan suomalaisessa muodossa
    print(f"Päivämäärä: {paiva.strftime('%d.%m.%Y')}")

def hae_aloitusaika(varaus):
    aika = varaus[3].replace(".", ":")
    print(f"Aloitusaika: {aika}")

def hae_tuntimaara(varaus):
    tunnit = int(varaus[4])
    print(f"Tuntimäärä: {tunnit}")

def hae_tuntihinta(varaus):
    hinta = float(varaus[5].replace(",", "."))
    print(f"Tuntihinta: {hinta:.2f} €".replace(".", ","))

def laske_kokonaishinta(varaus):
    tunti = float(varaus[5].replace(",", "."))
    tunnit = int(varaus[4])
    kokonaishinta = tunti * tunnit
    # Muutetaan suomalaiseksi desimaalipilkuksi
    hinta_str = f"{kokonaishinta:.2f}".replace(".", ",")
    print(f"Kokonaishinta: {hinta_str} €")

def hae_maksettu(varaus):
    arvo = varaus[6].strip().lower()
    #muutetaan True/False → Kyllä/Ei hyödynnetään if-else silmukkaa
    maksettu = "Kyllä" if arvo in ("true", "kyllä", "1") else "Ei"
    print(f"Maksettu: {maksettu}")

def hae_kohde(varaus):
    kohde = varaus[7]
    print(f"Kohde: {kohde}")

def hae_puhelin(varaus):
    puh = varaus[8]
    print(f"Puhelin: {puh}")

def hae_sahkoposti(varaus):
    sposti = varaus[9]
    print(f"Sähköposti: {sposti}")


def main(rivi_index=0):
    tiedosto = "varaukset.txt"

    with open(tiedosto, "r", encoding="utf-8") as f:
        rivit = f.readlines()

    rivit = [r.strip() for r in rivit if r.strip()]

    varausrivi = rivit[rivi_index]
    varaus = varausrivi.split('|')

    hae_varausnumero(varaus)
    hae_varaaja(varaus)
    hae_paiva(varaus)
    hae_aloitusaika(varaus)
    hae_tuntimaara(varaus)
    hae_tuntihinta(varaus)
    laske_kokonaishinta(varaus)
    hae_maksettu(varaus)
    hae_kohde(varaus)
    hae_puhelin(varaus)
    hae_sahkoposti(varaus)


if __name__ == "__main__":
    valinta = int(input("Anna rivinumero (0 = 1. varaus): "))
    main(valinta)
