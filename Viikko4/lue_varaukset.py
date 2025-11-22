"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
"""
from datetime import datetime

def muunna_varaustiedot(varaus: list) -> list:
    # Poistetaan turhat välilyönnit jokaisesta kentästä
    varaus = [alkio.strip() for alkio in varaus]

    # 0: varausId -> int
    varaus_id = int(varaus[0])

    # 1: nimi -> str
    nimi = varaus[1]

    # 2: sähköposti -> str
    sahkoposti = varaus[2]

    # 3: puhelin -> str (ei kannata muuttaa numeroksi)
    puhelin = varaus[3]

    # 4: varauksenPvm -> datetime.date (muoto: 2025-11-12)
    varauksen_pvm = datetime.strptime(varaus[4], "%Y-%m-%d").date()

    # 5: varauksenKlo -> datetime.time (muoto: 09:00)
    varauksen_klo = datetime.strptime(varaus[5], "%H:%M").time()

    # 6: varauksenKesto -> int (tunnit tms.)
    varauksen_kesto = int(varaus[6])

    # 7: hinta -> float (korjataan samalla suomalaisen merkistön desimaalipilkku
    hinta = float(varaus[7].replace(",", "."))

    # 8: varausVahvistettu -> bool (oletus "True"/"False")
    vahvistettu_str = varaus[8].strip().lower()
    if vahvistettu_str in ("true", "1", "kyllä", "yes"):
        varaus_vahvistettu = True
    else:
        varaus_vahvistettu = False

    # 9: varattuTila -> str
    varattu_tila = varaus[9]

    # 10: varausLuotu -> datetime (muoto: 2025-08-12 14:33:20)
    varaus_luotu = datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")

    muutettuvaraus = [
        varaus_id,
        nimi,
        sahkoposti,
        puhelin,
        varauksen_pvm,
        varauksen_klo,
        varauksen_kesto,
        hinta,
        varaus_vahvistettu,
        varattu_tila,
        varaus_luotu,
    ]

    return muutettuvaraus

def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def main():
    # HUOM! seuraaville riveille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    # Kutsutaan funkioita hae_varaukset, joka palauttaa kaikki varaukset oikeilla tietotyypeillä
    
    def otsikko(teksti, leveys=60):
        return teksti.center(leveys, "=")
    
    varaukset = hae_varaukset("varaukset.txt")
    print(" | ".join(varaukset[0]))
    print("------------------------------------------------------------------------")

    for varaus in varaukset[1:]:
        print(" | ".join(str(x) for x in varaus))
        tietotyypit = [type(x).__name__ for x in varaus]
        print(" | ".join(tietotyypit))
        print("------------------------------------------------------------------------")

 # 1) kaikki vahvistetut varaukset
    print("\n" + otsikko("1) Vahvistetut varaukset"))
    for varaus in varaukset[1:]:
        if varaus[8]:  # varausVahvistettu == True
            print(" | ".join(str(x) for x in varaus))

    # 2) yli 3h kestävät varaukset
    print("\n" + otsikko("2) Yli 3h kestävät varaukset"))
    for varaus in varaukset[1:]:
        if varaus[6] > 3:  # varauksenKesto > 3
            print(" | ".join(str(x) for x in varaus))

    # 3) varauksen vahvistusstatus (nimi + status)
    print("\n" + otsikko("3) Varausten vahvistusstatus"))
    for varaus in varaukset[1:]:
        nimi = varaus[1]
        status = "Vahvistettu" if varaus[8] else "Ei vahvistettu"
        print(f"{nimi}: {status}")

    # 4) yhteenveto vahvistuksista + 5) vahvistettujen kokonaistulo
    vahvistetut_lkm = 0
    ei_vahvistetut_lkm = 0
    vahvistettujen_tulo = 0.0

    for varaus in varaukset[1:]:
        if varaus[8]:
            vahvistetut_lkm += 1
            vahvistettujen_tulo += varaus[7]  # hinta
        else:
            ei_vahvistetut_lkm += 1

    print("\n" + otsikko("4) Yhteenveto vahvistuksista"))
    print(f"Vahvistettuja varauksia: {vahvistetut_lkm}")
    print(f"Vahvistamattomia varauksia: {ei_vahvistetut_lkm}")

    print("\n" + otsikko("5) Vahvistettujen varausten kokonaistulo"))
    # pilkku tuhaterottimena, kaksi desimaalia
    kokonaistulo_str = f"{vahvistettujen_tulo:,.2f}"
    print(f"{kokonaistulo_str} €")

if __name__ == "__main__":
    main()