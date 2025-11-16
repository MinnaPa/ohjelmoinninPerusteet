from datetime import datetime

def muotoile_paiva(pvm):
    # 2025-10-31 → 31.10.2025
    d = datetime.strptime(pvm, "%Y-%m-%d")
    return d.strftime("%d.%m.%Y")

def muotoile_hinta(euro):
    # 19.95 → 19,95 €
    return f"{float(euro):.2f}".replace(".", ",") + " €"

def laske_kokonaishinta(tunnit, tuntihinta):
    summa = float(tunnit) * float(tuntihinta)
    return f"{summa:.2f}".replace(".", ",") + " €"

def tulosta_varaukset(varaukset):
    # Otsikot
    otsikot = [
        "Varaus", "Varaaja", "Pvm", "Aika", "H", "Hinta/h",
        "KokHinta", "Maksettu", "Kohde", "Puhelin", "Sähköposti"
    ]

    # Sarakeleveydet
    leveydet = [8, 18, 12, 6, 4, 10, 12, 10, 15, 12, 25]

    # Otsikkorivi
    otsikkorivi = "".join(otsikot[i].ljust(leveydet[i]) for i in range(len(otsikot)))
    print(otsikkorivi)
    print("-" * sum(leveydet))

    # Tulostetaan varaukset
    for varaus in varaukset:
        numero, nimi, pvm, aika, tunnit, tuntihinta, maksettu, kohde, puh, sposti = varaus

        kokonaishinta = laske_kokonaishinta(tunnit, tuntihinta)

        rivi = (
            numero.ljust(8) +
            nimi.ljust(18) +
            muotoile_paiva(pvm).ljust(12) +
            aika.ljust(6) +
            tunnit.ljust(4) +
            muotoile_hinta(tuntihinta).ljust(10) +
            kokonaishinta.ljust(12) +
            ("Kyllä" if maksettu == "True" else "Ei").ljust(10) +
            kohde.ljust(15) +
            puh.ljust(12) +
            sposti.ljust(25)
        )

        print(rivi)

def main():
    tiedosto = "varaukset.txt"
    kaikki_varaukset = []

    # Luetaan kaikki varaukset tiedostosta
    with open(tiedosto, "r", encoding="utf-8") as f:
        for rivi in f:
            rivi = rivi.strip()
            if not rivi:
                continue
            osat = rivi.split("|")
            kaikki_varaukset.append(osat)

    tulosta_varaukset(kaikki_varaukset)

if __name__ == "__main__":
    main()
