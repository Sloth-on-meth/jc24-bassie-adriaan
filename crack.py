import zipfile
import argparse
import os
import shutil
import zlib
# Wachtwoordenlijst, handmatig opgehaald uit de afbeelding
passwords = [
    "Bassie", "en", "Adriaan", "Bas", "Aad", "van", "Toor", "wie", "in", "Nederlansk", "artysteduo",
    "Harren", "earste", "aktiviteiten", "under", "dizze", "namme", "wienen", "yn", "mar", "se",
    "waarden", "foaral", "ferneamd", "mei", "ferskate", "telefyzjesearjes", "en", "merchandising",
    "De", "telefyzjesearjes", "wienen", "ofgryslik", "populer", "en", "binne", "noch", "hieltyd",
    "ien", "fan", "de", "ferneamdste", "Nederlanske", "bernesearjes", "Wurkoersjoch", "In", "kar",
    "Telefyzjesearjes", "De", "telefyzjesearjes", "hawwe", "yn", "de", "rin", "fan", "de", "tiid",
    "ferskate", "neibewurkings", "han", "Bassie", "Adriaan", "De", "Plaaggeest", "Bassie", "Adriaan",
    "Het", "Geheim", "van", "de", "Sleutel", "Adriaan", "De", "Diamant", "Adriaan", "De", "Huilende",
    "Professor", "Leren", "Lachen", "met", "Bassie", "Adriaan", "en", "Bassie", "Adriaan", "Het",
    "Geheim", "van", "de", "Schatkaart", "Bassie", "Adriaan", "De", "Verdwenen", "Kroon", "Bassie",
    "Adriaan", "De", "Verzonken", "Stad", "Leren", "Lachen", "met", "Bassie", "Adriaan", "Bassie",
    "Adriaan", "De", "Geheimzinnige", "Opdracht", "Reis", "troch", "Europa", "Bassie", "Adriaan",
    "De", "Reis", "vol", "Verrassingen", "Reis", "troch", "Amearika", "Liedjes", "uit", "Grootmoeders",
    "Tijd", "útstjoerings", "In", "kar", "Hondert", "maal", "Bassie", "Adriaan", "alternative", "titel",
    "Winterpret", "Brieven", "aan", "de", "Koningin", "De", "Verdwenen", "Trosster", "De", "Stop-en-Stap-Sjo",
    "Leer", "het", "Verkeer", "it", "sirkus", "Bassie", "Adriaan", "in", "het", "circus", "it", "teater",
    "LIVE", "Jaar", "Theater", "Lachspektakelshow", "Bioskoopfilm", "Keet", "Koen", "en", "de", "Speurtocht",
    "naar", "Bassie", "Adriaan"
]
# Functie om het wachtwoord te testen en een zipbestand uit te pakken
def test_passwords(zip_file, password_list):
    with zipfile.ZipFile(zip_file, 'r') as zf:
        for password in password_list:
            try:
                # Probeer het wachtwoord
                zf.extractall(pwd=bytes(password, 'utf-8'))
                print(f"[+] Wachtwoord gevonden: {password}")
                return password
            except (RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile, zlib.error) as e:
                # Fout bij het kraken, probeer het volgende wachtwoord
                print(f"[-] Wachtwoord mislukt: {password}, fout: {e}")
                continue
    print("[-] Geen wachtwoord gevonden")
    return None

# Functie om door meerdere lagen zip-bestanden te kraken en elk bestand op te slaan
def crack_multiple_layers(zip_file_path, passwords):
    current_zip = zip_file_path

    while True:
        print(f"[*] Bezig met kraken van: {current_zip}")
        password = test_passwords(current_zip, passwords)

        if password is None:
            print(f"[-] Geen wachtwoord gevonden voor {current_zip}. Stopping.")
            break
        
        # Pak het volgende zip-bestand uit, indien aanwezig
        with zipfile.ZipFile(current_zip, 'r') as zf:
            file_list = zf.namelist()
            next_zip_file = None

            # Zoek naar een nieuw zip-bestand in het uitgepakte bestand
            for file in file_list:
                if file.endswith('.zip'):
                    next_zip_file = file
                    break

            if next_zip_file:
                # Pak het volgende zip-bestand uit
                print(f"[+] Gevonden nieuw zip-bestand: {next_zip_file}")
                zf.extract(next_zip_file, pwd=bytes(password, 'utf-8'))

                # Hernoem het uitgepakte zipbestand om het op te slaan als onversleuteld
                new_filename = f"unpacked_{password}_{os.path.basename(next_zip_file)}"
                shutil.move(next_zip_file, new_filename)
                print(f"[+] Zipbestand opgeslagen als: {new_filename}")

                # Ga verder met het nieuwe zipbestand
                current_zip = new_filename
            else:
                print("[*] Geen nieuwe zip-bestanden gevonden. Proces voltooid!")
                break

if __name__ == "__main__":
    # Gebruik argparse om een command line argument voor het zipbestand te accepteren
    parser = argparse.ArgumentParser(description="Kraak zip-bestanden in meerdere lagen.")
    parser.add_argument("zipfile", help="Het pad naar het eerste zipbestand")
    args = parser.parse_args()

    # Start met het opgegeven zipbestand
    crack_multiple_layers(args.zipfile, passwords)
