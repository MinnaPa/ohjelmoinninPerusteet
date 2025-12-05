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

"""Tämä osa ohjelma lukee ja käsittelee dataa.
utf-8 on hyvä ottaa huomioon, jotta erikoisrmerkit ja skandit toimivat tarvittaessa oikein. Päivämäärien tunnistamiseen käytetään
aika-oliota, joka ymmärtää ajan käsitteenä, eikä pelkkänä merkkijonona. Python myös käyttää erottimena pistettä, ja tiedostossa on käytössä
pilkku, joten sekin huomioidaan tässä osassa. Varalla myös tuo virherivi, jos tiedoston lukeminen epäonnistuu jostain syystä."""
def lue_data(tiedostonimi):
    mittaukset = [] 
    try:
        with open(tiedostonimi, 'r', encoding='utf-8') as tiedosto:
            lukija = csv.reader(tiedosto, delimiter=';')
            next(lukija)
            for rivi in lukija:
                aikaleima_str = rivi[0][:19] 
                aika_olio = datetime.strptime(aikaleima_str, "%Y-%m-%dT%H:%M:%S")
                kulutus = float(rivi[1].replace(",", "."))
                mittaukset.append({"pvm": aika_olio, "kulutus": kulutus})
    except Exception as e:
        print(f"Virhe tiedoston luvussa: {e}")
    return mittaukset

# --- ANALYYSILOGIIKKA --- 
""" Tämä ohjelman osa luo vuosi, kuukausi tai päiväraportin käyttäjän antaman käskyn mukaan"""
def luo_vuosiraportti(data):
    kokonaissumma = sum(m['kulutus'] for m in data)
    raportti = f"--- VUOSIRAPORTTI 2025 ---\nKokonaiskulutus: {kokonaissumma:.2f} kWh\nMittauksia: {len(data)} kpl\n"
    return raportti

def luo_kuukausiraportti(data, haluttu_kk):
    kk_summa = sum(m['kulutus'] for m in data if m['pvm'].month == haluttu_kk)
    kk_nimet = ["", "Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu", 
                "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]
    return f"--- KUUKAUSIRAPORTTI ({kk_nimet[haluttu_kk]}) ---\nKuukauden kulutus: {kk_summa:.2f} kWh\n"

def luo_paivaraportti(data, alku_pvm, loppu_pvm):
    paiva_summat = {}
    for m in data:
        if alku_pvm <= m['pvm'] <= loppu_pvm:
            paiva_avain = m['pvm'].strftime("%d.%m.%Y")
            paiva_summat[paiva_avain] = paiva_summat.get(paiva_avain, 0) + m['kulutus']
    
    raportti = f"--- PÄIVÄRAPORTTI ({alku_pvm.strftime('%d.%m.')} - {loppu_pvm.strftime('%d.%m.')}) ---\n"
    for pvm, summa in paiva_summat.items():
        raportti += f"{pvm}: {summa:.2f} kWh\n"
    if not paiva_summat: raportti += "Ei dataa tällä aikavälillä.\n"
    return raportti

# --- PÄÄOHJELMA ---
"""Tämä osa ohjelmaa kysyy ensin käyttäjältä, mitä käyttäjä haluaa tehdä. Käyttäjän valinnan mukaan
luodaan päivä, kuukausi tai vuosiraportti. Lopuksi käyttäjältä kysytään, haluaako hän tallentaa raportin tiedostoon. Raportti tallentuu sen mukaan 
nimellä raportti1/2/3.txt, mitä käyttäjä on valinnut. Ohjelma uudelleenkirjoittaa saman tiedoston, mikäli käyttäjä pyytää
esim päiväraporttia. Ohjelma toimii niin kauan, kunnes käyttäjä antaa lopettamiskomennon."""

def main():
    print("Luetaan tiedostoa...")
    mittausdata = lue_data("2025.csv")
    print(f"Data luettu! Rivejä: {len(mittausdata)}\n")

    viimeisin_raportti = "" 
    tallennettava_tiedosto = ""  # UUSI MUUTTUJA: Tähän muistetaan tiedostonimi eli esim raportti1.txt

    while True:
        print("\nValitse raporttityyppi:")
        print("1) Päiväkohtainen yhteenveto (Tallentuu: raportti1.txt)")
        print("2) Kuukausikohtainen yhteenveto (Tallentuu: raportti2.txt)")
        print("3) Vuosiyhteenveto (Tallentuu: raportti3.txt)")
        print("4) Lopeta ohjelma")
        
        valinta = input("Valintasi: ")
        
        if valinta == "1":
            print("Anna aikaväli (muodossa PP.KK.VVVV)")
            try:
                alku_str = input("Alkupäivä: ")
                loppu_str = input("Loppupäivä: ")
                alku = datetime.strptime(alku_str, "%d.%m.%Y")
                loppu = datetime.strptime(loppu_str + " 23:59", "%d.%m.%Y %H:%M")
                
                viimeisin_raportti = luo_paivaraportti(mittausdata, alku, loppu)
                
                # Asetetaan tiedostonimi valinnan mukaan
                tallennettava_tiedosto = "raportti1.txt" 
                
                print("\n" + viimeisin_raportti)
            except ValueError:
                print("Virheellinen päivämäärämuoto!")
                continue

        elif valinta == "2":
            try:
                kk = int(input("Anna kuukausi (1-12): "))
                if 1 <= kk <= 12:
                    viimeisin_raportti = luo_kuukausiraportti(mittausdata, kk)
                    
                    # Asetetaan tiedostonimi valinnan mukaan
                    tallennettava_tiedosto = "raportti2.txt"
                    
                    print("\n" + viimeisin_raportti)
                else:
                    print("Virhe: Anna luku väliltä 1-12.")
                    continue
            except ValueError:
                print("Virhe: Anna numero.")
                continue

        elif valinta == "3":
            viimeisin_raportti = luo_vuosiraportti(mittausdata)
            
            # Asetetaan tiedostonimi valinnan mukaan
            tallennettava_tiedosto = "raportti3.txt"
            
            print("\n" + viimeisin_raportti)

        elif valinta == "4":
            print("Kiitos ja näkemiin!")
            break
        else:
            print("Tuntematon valinta.")
            continue

        # --- TALLENNUSVALIKKO ---
        if viimeisin_raportti:
            while True:
                # Näytetään käyttäjälle mihin tiedostoon ollaan tallentamassa
                print(f"\nMitä haluat tehdä seuraavaksi?")
                print(f"1) Kirjoita raportti tiedostoon ({tallennettava_tiedosto})")
                print("2) Luo uusi raportti")
                print("3) Lopeta")
                
                jatko = input("Valinta: ")
                
                if jatko == "1":
                    try:
                        # Käytetään nyt muuttujaa 'tallennettava_tiedosto' ja kerrotaan, että tallennus on tehty
                        with open(tallennettava_tiedosto, "w", encoding="utf-8") as f:
                            f.write(viimeisin_raportti)
                        print(f"✅ Raportti tallennettu tiedostoon: {tallennettava_tiedosto}")
                    except Exception as e:
                        print(f"Tallennus epäonnistui: {e}")
                    
                elif jatko == "2":
                    break 
                elif jatko == "3":
                    print("Ohjelma lopetetaan.")
                    return 
                else:
                    print("Tuntematon valinta.")

if __name__ == "__main__":
    main()