# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

"""Tässä koodissa käytän sanakirjoja (dict).
Se on selkeämpi kuin pelkät listat, koska koodia lukiessa näkee heti,
mitä tietoa käsitellään (esim. varaus["hinta"] vs varaus[7]).
Koodia on helpompi ylläpitää, kun ei tarvitse muistaa indeksinumeroita, vaan näkee suoraan muuttujien nimet.
Jos luodaan hieman kehittyneempi ohjelma järkevämpää olisi käyttää olioita, 
sillä niiden kirjoittaminen on nopeampaa ja esim. vs code osaa auttaa olioiden kanssa paremmin.
Tässä harjoituksessa keskitytään kuitenkin sanakirjoihin, joten halusin harjoitella myös sen käyttöä. 
Tein erillisen kokeilun olioilla."""


from datetime import datetime

def muunna_varaustiedot(varaus: list) -> dict:
    # Luodaan ja palautetaan sanakirja. 
    return {
        "id": int(varaus[0]),
        "nimi": varaus[1],
        "sahkoposti": varaus[2],
        "puhelin": varaus[3],
        "pvm": datetime.strptime(varaus[4], "%Y-%m-%d").date(),
        "klo": datetime.strptime(varaus[5], "%H:%M").time(),
        "kesto": int(varaus[6]),
        "hinta": float(varaus[7]),
        "vahvistettu": varaus[8].lower() == "true",
        "tila": varaus[9],
        "luotu": datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")
    }

def hae_varaukset(varaustiedosto: str) -> list:
    varaukset = []
    # POISTETTU: varaukset.append(["varausId"...]) rivi tästä
    
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            # Funktio palauttaa sanakirjan, joka lisätään listaan
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def vahvistetut_varaukset(varaukset: list):
    # HUOM: Ei enää [1:], vaan käydään koko lista läpi (ohjelma kaatuu, jos yrittää numeroin käydä läpi)
    for varaus in varaukset:
        if(varaus["vahvistettu"]):
            # Käytetään avaimia indeksien sijaan
            print(f"- {varaus['nimi']}, {varaus['tila']}, {varaus['pvm'].strftime('%d.%m.%Y')} klo {varaus['klo'].strftime('%H.%M')}")
    print()

def pitkat_varaukset(varaukset: list):
    for varaus in varaukset:
        if(varaus["kesto"] >= 3):
            print(f"- {varaus['nimi']}, {varaus['pvm'].strftime('%d.%m.%Y')} klo {varaus['klo'].strftime('%H.%M')}, kesto {varaus['kesto']} h, {varaus['tila']}")
    print()

def varausten_vahvistusstatus(varaukset: list):
    for varaus in varaukset:
        if(varaus["vahvistettu"]):
            print(f"{varaus['nimi']} → Vahvistettu")
        else:
            print(f"{varaus['nimi']} → EI vahvistettu")
    print()

def varausten_lkm(varaukset: list):
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset:
        if(varaus["vahvistettu"]):
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1

    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: list):
    varaustenTulot = 0
    for varaus in varaukset:
        if(varaus["vahvistettu"]):
            # Lasketaan kesto * hinta selkeillä avaimilla
            varaustenTulot += varaus["kesto"] * varaus["hinta"]

    print("Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€")
    print()

    print("Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€")
    print()

def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()