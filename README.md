# ⚠️ Denne README er lavet af Lumo AI (Proton), og tilpasset af Nicolai Martini.
<br>

<br>

# Rema 1000 Digital Forensics Project

Dette projekt er en del af afgangsprojektet for uddannelsen som IT-teknolog på erhvervsakademiet. Projektet omhandler digital efterforskning af Android-appen "Rema 1000 | Scan & Go", baseret på datasikringer opnået via Cellebrite UFED (After First Unlock).

Formålet er at udvikle værktøjer til at udtrække, analysere og visualisere forbrugeradfærd og transaktionshistorik fra appens SQLite-databaser.

## 📁 Projektstruktur

Projektet er opdelt i moduler, der hver især adresserer specifikke krav til dataudtrækning og analyse:

- **`backend.py`**: Kernebibliotek indeholdende funktioner til at håndtere ZIP-arkiver, finde og ektrahere SQLite-databaser samt læse tabelstrukturer og indhold.
- **`krav_01.py` & `krav_02.py`**: Scripts til at udtrække specifikke databaser fra en AFU-arkiv (zip) til enten midlertidig lagerplads eller en brugerdefineret sti.
- **`krav_03.py`**: Script til at udforske databasernes struktur (tabeller og kolonner) og indhold.
- **`krav_04.py`**: Filtrering af data til kun at inkludere efterforskningsrelevant information (f.eks. kvitteringer).
- **`krav_05.py`**: Databearbejdning for at gøre informationen menneskelæsbar (konvertering af Unix-tidsstempler, normalisering af produktnavne).
- **`krav_06.py`**: Implementering af en rå ALEAPP-artefakt (`rema1000_receipt_raw`) til integration i forensiske værktøjer.
- **`krav_07.py`**: Implementering af en bearbejdet ALEAPP-artefakt (`rema1000_receipt_prettified`) med humanreadable data og filtrering af irrelevante felter.
- **`krav_08.py`**: Generering af terminal-output med oversigt over besøgte butikker baseret på transaktionsdata.
- **`krav_09.py`**: Visualisering af besøgte butikker på et interaktivt OpenStreetMap-kort (via Folium).
- **`krav_10.py`**: Udvidet kortvisualisering, der inkluderer antal besøg, datoer og tidspunkter for hver butik.
- **`requirements.txt`**: Liste over nødvendige Python-pakker.

## 🛠️ Installation og Krav

For at køre dette projekt kræves det følgende:

- **Python 3.10+** (anbefalet)
- **Pip** til pakkehåndtering

Installér de nødvendige afhængigheder:

```bash
pip install -r requirements.txt
```
Bemærk: Dette projekt kræver en gyldig AFU.zip fil (Cellebrite After First Unlock dump) placeret i samme mappe som scriptsene, eller at stien justeres i koden.



## 🚀 Brugervejledning  
### Grundlæggende Dataudtrækning  
Kør scriptsene i rækkefølge for at gennemgå dataanalysen:

### 1. Ekstraktion:
```
python krav_01.py  # Til midlertidig mappe  
python krav_02.py  # Til specifik mappe
```

### 2. Analyse og Filtrering:
```
python krav_03.py  # Udforsk struktur
python krav_04.py  # Filtrer relevante data
python krav_05.py  # Humanreadable output
```

### 3. Visualisering:
```
python krav_08.py  # Terminal oversigt
python krav_09.py  # Basis kort
python krav_10.py  # Detaljeret kort med statistik
```

## Integration med ALEAPP
For at bruge artefakterne (krav_06.py og krav_07.py) i ALEAPP:
1. Kopier .py filerne til ALEAPP's scripts/artifacts mappe.
2. Kør ALEAPP som normalt.  

Artefakterne vil blive registreret under kategorien "EK F2026 IoT4 NM".
## 🔍 Funktioner
<b>Automatisk Database Discovery</b>: Bruger regulære udtryk til at finde specifikke .db filer i komplekse arkivstrukturer.  
<b>Tidskonvertering</b>: Automatisk konvertering af millisekund-baserede tidsstempler til lokal tid (Europe/Copenhagen).  
<b>Produktmatchning</b>: Sammenligner kvitteringslinjer med produktbasen for at identificere købt varer.  
<b>Geolokalisering</b>: Integrerer GPS-koordinater fra databasen med Folium-kort til visuel analyse af bevægelsesmønstre.  
## ⚠️ Bemærkninger og Begrænsninger
<b>Datakilder</b>: Koden forventer en specifik databasestruktur (ReceiptEntity, ProductEntity, StoreEntity). Ændringer i app-versioner kan påvirke kompatibiliteten.  
<b>Ydeevne</b>: Ved meget store datasæt kan krav_10.py tage længere tid at generere pga. mange databaseopslag i løkker.  
<b>Sikkerhed</b>: Koden håndterer følsomme betalingsdata (PAN, card type). Sørg for at slette midlertidige filer efter brug.  
## 📄 Licens og Brug
Dette projekt er udarbejdet i et akademisk øjemed. Koden må bruges til læring og forskning, men skal citeres korrekt.  

Udarbejdet af Nicolai Martini - IT-teknologuddannelsen, 2026