"""
MIT License

Copyright (c) 2025 Minna Parkkila

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import csv
from datetime import datetime

# Vaatimus: Funktio, docstring ja tietotyyppivihjeet (str -> list)
def lue_tiedosto(tiedostonimi: str) -> list:
    """
    Lukee CSV-tiedoston ja palauttaa sen sisällön listana.
    Käsittelee tyhjän tiedoston virheen.
    """
    rivi_lista = []
    try:
        with open(tiedostonimi, mode='r', encoding='utf-8') as tiedosto:
            lukija = csv.reader(tiedosto, delimiter=';')
            
            try:
                # Ohitetaan otsikkorivi
                next(lukija) 
            except StopIteration:
                print(f"Virhe: Tiedosto '{tiedostonimi}' on tyhjä!") #jos tiedosto ei sisällä mitään
                return []

            # Vaatimus: Toistorakenne (for) rivien läpikäyntiin
            for rivi in lukija:
                if rivi: 
                    rivi_lista.append(rivi)
                    
    except FileNotFoundError:
        print(f"Virhe: Tiedostoa '{tiedostonimi}' ei löytynyt.") #jos tiedosto on väärässä paikassa
        return []
    
    return rivi_lista

# Vaatimus: Tietotyyppivihjeet (list -> dict)
def laske_vaiheittain(data: list) -> dict:
    """
    Laskee summat erikseen jokaiselle vaiheelle (1, 2, 3).
    Palauttaa sanakirjan, jossa avaimena pvm ja arvona lista lukuja.
    """
    # Vaatimus: Muuttujat ja tietorakenteet (sanakirja)
    paivat = {} 

    for rivi in data:
        aikaleima_str = rivi[0] 
        pvm_obj = datetime.strptime(aikaleima_str, "%Y-%m-%dT%H:%M:%S")
        pvm_avain = pvm_obj.strftime("%Y-%m-%d")

        try:
            # Muutetaan arvot kokonaisluvuiksi
            k1 = int(rivi[1])
            k2 = int(rivi[2])
            k3 = int(rivi[3])
            t1 = int(rivi[4])
            t2 = int(rivi[5])
            t3 = int(rivi[6])
            
        except ValueError:
            continue 

        # Vaatimus: Ehtolause (if) päivien ryhmittelyyn
        if pvm_avain not in paivat:
            # Vaatimus: Listat tietorakenteena [k1, k2, k3, t1, t2, t3]
            paivat[pvm_avain] = [0, 0, 0, 0, 0, 0]
            
        # Päivitetään summat listaan
        paivat[pvm_avain][0] += k1
        paivat[pvm_avain][1] += k2
        paivat[pvm_avain][2] += k3
        paivat[pvm_avain][3] += t1
        paivat[pvm_avain][4] += t2
        paivat[pvm_avain][5] += t3
        
    return paivat

def etsi_paras_paiva(paiva_data: dict) -> str:
    """
    Etsii päivän, jolloin nettokulutus (kulutus - tuotanto) oli pienin.
    Palauttaa päivämäärä-avaimen.
    """
    paras_pvm = ""
    pienin_netto = float('inf') # Alustetaan äärettömällä

    for pvm, arvot in paiva_data.items():
        # Lasketaan kaikkien vaiheiden kulutus ja tuotanto yhteen
        kokonais_kulutus = sum(arvot[0:3])
        kokonais_tuotanto = sum(arvot[3:6])
        netto = kokonais_kulutus - kokonais_tuotanto

        # Etsitään pienin arvo
        if netto < pienin_netto:
            pienin_netto = netto
            paras_pvm = pvm
            
    return paras_pvm

def muotoile_luku(arvo_wh: int) -> str:
    """Muuttaa Wh -> kWh, pyöristää ja vaihtaa pisteen pilkuksi."""
    kwh = arvo_wh / 1000
    return f"{kwh:.2f}".replace('.', ',')

def tulosta_raportti(paiva_data: dict):
    """Tulostaa raportin ja korostaa parhaan päivän."""
    
    viikonpaivat = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
    
    # Selvitetään "paras päivä" korostusta varten
    #ekopaiva = etsi_paras_paiva(paiva_data) testattu, toimii, kommentoitu pois

    print("\nViikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)")
    #print("(* = Viikon pienin nettokulutus)\n") osa poiskommentoitua osaa
    
    print(f"{'Päivä':<13} {'Pvm':<12} {'Kulutus [kWh]':<26} {'Tuotanto [kWh]':<26}")
    print(f"{'':<13} {'(pv.kk.vvvv)':<12} {'v1':<8} {'v2':<8} {'v3':<8} {'v1':<8} {'v2':<8} {'v3':<8}")
    print("-" * 75)

    for pvm_iso in sorted(paiva_data.keys()):
        arvot = paiva_data[pvm_iso]
        dt = datetime.strptime(pvm_iso, "%Y-%m-%d")
        viikonpaiva_nimi = viikonpaivat[dt.weekday()]
        suomi_pvm = dt.strftime("%d.%m.%Y")
        
        # Muotoillaan luvut
        k1_str = muotoile_luku(arvot[0])
        k2_str = muotoile_luku(arvot[1])
        k3_str = muotoile_luku(arvot[2])
        t1_str = muotoile_luku(arvot[3])
        t2_str = muotoile_luku(arvot[4])
        t3_str = muotoile_luku(arvot[5])

        # Tämä liittyy bonukseen, eli parhaan päivän merkintään
        merkki = ""
       #if pvm_iso == ekopaiva:
        #    merkki = "*" 

        #Lisätään merkki viikonpäivän nimen eteen (kommenotoitu pois, eli ei tee tätä)
        print(f"{merkki + viikonpaiva_nimi:<13} {suomi_pvm:<12} {k1_str:<8} {k2_str:<8} {k3_str:<9} {t1_str:<8} {t2_str:<8} {t3_str:<8}")

    print("-" * 75)

if __name__ == "__main__":
    tiedosto = "viikko42.csv"
    data = lue_tiedosto(tiedosto)
    
    if data:
        lasketut = laske_vaiheittain(data)
        tulosta_raportti(lasketut)