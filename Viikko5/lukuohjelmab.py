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

def lue_tiedosto(tiedostonimi: str) -> list:
    """Lukee CSV-tiedoston ja palauttaa sen sisällön listana.
    Huomioi tyhjän tiedoston sekä virheellisen tiedostosijainnin mahdollisuudet. Ohittaa otsikkorivin.
    """
    rivi_lista = []
    try:
        with open(tiedostonimi, mode='r', encoding='utf-8') as tiedosto:
            lukija = csv.reader(tiedosto, delimiter=';')
            try:
                next(lukija) 
            except StopIteration:
                print(f"--> Varoitus: Tiedosto '{tiedostonimi}' on tyhjä.")
                return []

            for rivi in lukija:
                if rivi: 
                    rivi_lista.append(rivi)
                    
    except FileNotFoundError:
        print(f"--> Varoitus: Tiedostoa '{tiedostonimi}' ei löytynyt.")
        return []
    
    return rivi_lista

def laske_vaiheittain(data: list) -> dict:
    """Laskee summat erikseen jokaiselle vaiheelle."""
    paivat = {} 

    for rivi in data:
        try:
            aikaleima_str = rivi[0] 
            pvm_obj = datetime.strptime(aikaleima_str, "%Y-%m-%dT%H:%M:%S")
            pvm_avain = pvm_obj.strftime("%Y-%m-%d")

            k1 = int(rivi[1])
            k2 = int(rivi[2])
            k3 = int(rivi[3])
            t1 = int(rivi[4])
            t2 = int(rivi[5])
            t3 = int(rivi[6])
            
        except (ValueError, IndexError):
            continue 

        if pvm_avain not in paivat:
            paivat[pvm_avain] = [0, 0, 0, 0, 0, 0]
            
        paivat[pvm_avain][0] += k1
        paivat[pvm_avain][1] += k2
        paivat[pvm_avain][2] += k3
        paivat[pvm_avain][3] += t1
        paivat[pvm_avain][4] += t2
        paivat[pvm_avain][5] += t3
        
    return paivat

def etsi_paras_paiva(paiva_data: dict) -> str:
    """
    Etsii päivän, jolloin nettokulutus oli pienin, osa bonusta. 
    Tämä on helpompi kommentoida näin ja antaa pyöriä,
    tulostus kommentoitu pois myöhemmiin
    """
    paras_pvm = ""
    pienin_netto = float('inf')

    for pvm, arvot in paiva_data.items():
        kokonais_kulutus = sum(arvot[0:3])
        kokonais_tuotanto = sum(arvot[3:6])
        netto = kokonais_kulutus - kokonais_tuotanto

        if netto < pienin_netto:
            pienin_netto = netto
            paras_pvm = pvm
            
    return paras_pvm

def muotoile_luku(arvo_wh: int) -> str:
    """Muuttaa Wh -> kWh, pyöristää ja vaihtaa pisteen pilkuksi."""
    kwh = arvo_wh / 1000
    return f"{kwh:.2f}".replace('.', ',')

import sys # Tarvitaan oletustulostusta varten

def tulosta_raportti(paiva_data: dict, otsikko: str, kohde=sys.stdout):
    """
    Tulostaa raportin annettuun kohteeseen.
    """
    viikonpaivat = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
    ekopaiva = etsi_paras_paiva(paiva_data)

    # Huomaa: file=kohde ohjaa tekstin tiedostoon, jos sellainen on annettu
    print("\n" + "=" * 75, file=kohde)
    print(f"{otsikko} (kWh, vaiheittain)", file=kohde)
    #print("(* = Tämän viikon pienin nettokulutus)", file=kohde) kommentoitu pois, osa bonusta
    print("=" * 75, file=kohde)
    
    print(f"{'Päivä':<13} {'Pvm':<12} {'Kulutus [kWh]':<26} {'Tuotanto [kWh]':<26}", file=kohde)
    print(f"{'':<13} {'(pv.kk.vvvv)':<12} {'v1':<8} {'v2':<8} {'v3':<8} {'v1':<8} {'v2':<8} {'v3':<8}", file=kohde)
    print("-" * 75, file=kohde)

    for pvm_iso in sorted(paiva_data.keys()):
        arvot = paiva_data[pvm_iso]
        dt = datetime.strptime(pvm_iso, "%Y-%m-%d")
        viikonpaiva_nimi = viikonpaivat[dt.weekday()]
        suomi_pvm = dt.strftime("%d.%m.%Y")
        
        k1_str = muotoile_luku(arvot[0])
        k2_str = muotoile_luku(arvot[1])
        k3_str = muotoile_luku(arvot[2])
        t1_str = muotoile_luku(arvot[3])
        t2_str = muotoile_luku(arvot[4])
        t3_str = muotoile_luku(arvot[5])

        #Tämä on osa sitä bonusta
        merkki = ""
        #if pvm_iso == ekopaiva: tämäkin kommentoitu pois, osa bonusta
            #merkki = "*"  tämä myös pois kommentoitu

        print(f"{merkki + viikonpaiva_nimi:<13} {suomi_pvm:<12} {k1_str:<8} {k2_str:<8} {k3_str:<9} {t1_str:<8} {t2_str:<8} {t3_str:<8}", file=kohde)

    print("-" * 75, file=kohde)
    print("\n", file=kohde)

# --- Pääohjelma ---
if __name__ == "__main__":
    tiedostot = ["viikko41.csv", "viikko42.csv", "viikko43.csv"]
    
    print(f"Luetaan tiedostoja ja kirjoitetaan raportti tiedostoon 'yhteenveto.txt'")

    # Avataan tiedosto kirjoitusta varten, ääkköset huomioitu
    with open("yhteenveto.txt", "w", encoding="utf-8") as tulostustiedosto:
        
        for tiedosto in tiedostot:
            raakadata = lue_tiedosto(tiedosto)
            
            if raakadata:
                siisti_nimi = tiedosto.replace(".csv", "").capitalize()
                raportin_otsikko = f"{siisti_nimi} sähkönkulutus ja -tuotanto"
                
                lasketut = laske_vaiheittain(raakadata)
                
                # Kutsutaan funktiota ja annetaan kohde-parametriksi avattu tiedosto
                tulosta_raportti(lasketut, raportin_otsikko, kohde=tulostustiedosto)
            else:
                # Virheet voi edelleen tulostaa ruudulle (ei anneta kohde-parametria)
                print(f"Huomio: Tiedostosta {tiedosto} ei saatu dataa.")

    print("Valmis! Tarkista tiedosto 'yhteenveto.txt'.")