# Kissakahvilasivusto

Tämä projekti on kissakahvilasivusto, jonka tarkoituksena on hallita varauksia, käyttäjiä ja kommentteja. Sivuston avulla käyttäjät voivat tehdä varauksia, tarkastella niitä, muokata ja poistaa varauksia, lisätä kommentteja ja rekisteröityä sekä kirjautua sisään.

## Käytetyt teknologiat

- **Flask**: Web-kehys, joka on käytetty palvelimen ja sivuston logiikan luomiseen.
- **SQLite**: Tietokanta, jossa tallennetaan käyttäjien tiedot, varaukset, kommentit ja luokat.
- **HTML**: Sivuston rakenteen ja ulkoasun määrittelyyn.
- **Werkzeug**: Käytetty käyttäjän salasanojen turvalliseen käsittelyyn ja vertailuun.
- **Jinja2**: HTML-sivujen dynaaminen luominen Flaskin kanssa.

## Sivuston toiminnot

Sivusto tarjoaa seuraavat ominaisuudet:

- **Rekisteröityminen ja kirjautuminen**: Käyttäjät voivat luoda tilin ja kirjautua sisään käyttäen salasanaa. Salasanat tallennetaan suojattuna.
- **Varauksien hallinta**:
  - Käyttäjät voivat luoda, muokata ja poistaa varauksia.
  - Varausten luokittelu: Varauksille voidaan määrittää luokat, kuten "Eko", "Tavallinen" ja "Vippi".
  - Varausten ja niiden luokkien tallentaminen tietokantaan.
- **Kommentointi**: Käyttäjät voivat lisätä kommentteja varauksiinsa.
- **Varauksien haku**: Käyttäjät voivat etsiä varauksia nimen tai kategorian perusteella.
- **Turvallisuus**: Sisäänkirjautuminen vaatii käyttäjänimellä ja salasanalla autentikoinnin. Salausten käsittely tapahtuu turvallisesti käyttäen `werkzeug`-kirjastoa.

## Turvallisuus

Sivusto käyttää useita turvatoimia käyttäjien tietojen suojaamiseksi:

- **Salasanan suolaus ja hash**: Käyttäjien salasanat tallennetaan suolatulla ja hashatulla muodolla `werkzeug`-kirjaston avulla. Tämä estää salasanojen suoran paljastamisen tietokannassa.
- **Autentikointi ja istunnot**: Sivusto käyttää Flaskin `session`-mekanismia varmistaakseen, että vain kirjautuneet käyttäjät voivat tehdä varauksia, muokata niitä tai lisätä kommentteja.
- **Syötteiden validointi**: Käyttäjän syötteet tarkistetaan, kuten varauksen nimi, määrä ja aika, jotta vältetään virheelliset ja haitalliset syötteet.
- **SQL-injektioiden estäminen**: SQL-kyselyt suoritetaan käyttäen parametrisoituja kyselyjä, mikä estää SQL-injektiohyökkäykset.

## Asennusohjeet
1. **Kloonaa projekti**:
git clone <projekti-URL>


2. **Alusta tietokanta**:
Käytä `schema.sql`-tiedostoa tietokannan rakenteen alustamiseen:
sqlite3 database.db < schema.sql


Lisäksi voit alustaa testitiedot käyttämällä `init.sql`-tiedostoa:
sqlite3 database.db < init.sql

4. **Käynnistä palvelin**:
python app.py

## Kehittäminen ja laajennukset

- Lisäominaisuuksien ja virheiden korjausten kehittäminen on tervetullutta.
- Ehdotuksia parannuksista voidaan tehdä avaamalla issue tai tekemällä pull request.
