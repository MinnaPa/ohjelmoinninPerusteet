"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""

def main():
    varaukset = "varaukset.txt"

    # Luetaan tiedosto
    with open(varaukset, "r", encoding="utf-8") as f:
        rivi = f.read().strip()

    # Pilkotaan tiedot
    tiedot = rivi.split("|")

    # Määritellään nimetyt muuttujat
    varausnumero = tiedot[0]
    varaaja = tiedot[1]
    paivamaara = tiedot[2].replace("-", ".")
    aloitusaika = tiedot[3].replace(":", ".")
    tuntimaara = int(tiedot[4])
    tuntihinta = float(tiedot[5])
    maksettu = "Kyllä" if tiedot[6] == "True" else "Ei"
    kohde = tiedot[7]
    puhelin = tiedot[8]
    sahkoposti = tiedot[9]

    kokonaishinta = tuntimaara * tuntihinta

    # Määritellään tiedot sanakirjana (helpompi tulostaa siististi)
    varaus = {
        "Varausnumero": varausnumero,
        "Varaaja": varaaja,
        "Päivämäärä": paivamaara,
        "Aloitusaika": aloitusaika,
        "Tuntimäärä": tuntimaara,
        "Tuntihinta": f"{tuntihinta:.2f} €",
        "Kokonaishinta": f"{kokonaishinta:.1f} €",
        "Maksettu": maksettu,
        "Kohde": kohde,
        "Puhelin": puhelin,
        "Sähköposti": sahkoposti
    }

    # Tulostetaan tasaus (kentät 12 merkkiä leveitä vasemmalla) 
    # tämä siis lisäys, että tulostus olisi siistimpää :D 
    for otsikko, arvo in varaus.items():
        print(f"{otsikko+':':<13} {arvo}")


if __name__ == "__main__":
    main()


    # Kokeile näitä
    #print(varaus.split('|'))
    #varausId = varaus.split('|')[0]
    #print(varausId)
    #print(type(varausId))
    """
    Edellisen olisi pitänyt tulostaa numeron 123, joka
    on oletuksena tekstiä.

    Voit kokeilla myös vaihtaa kohdan [0] esim. seuraavaksi [1]
    ja testata mikä muuttuu
    """

if __name__ == "__main__":
    main()