# jakubsevela.cz

Osobní web Jakuba Ševely — specialista na Helios iNuvio. Hub v architektuře hub-and-spoke;
produktové weby [ethel.cz](https://ethel.cz) a [feedco.cz](https://feedco.cz) stojí samostatně.

Statický web bez buildu. Nasazuje GitHub Pages z branch `main`, root.

## Struktura

```
index.html            celá stránka — HTML, inline CSS, inline JS
brand/
  tokens.css          zdroj pravdy pro barvy, typografii, radiusy
  index.html          grafický manuál (v1.1) — paleta, wordmark, komponenty, kontrasty
images/reference/     fotky u referencí
scripts/
  build-fonts.js      self-hosting Google Fonts do /fonts/
CNAME                 jakubsevela.cz
.nojekyll             vypíná Jekyll — bez toho Pages ignoruje soubory s podtržítkem
robots.txt
sitemap.xml
CLAUDE.md             pravidla pro práci v repu (brand, texty, co nedělat)
```

## Lokální náhled

```bash
python3 -m http.server 8000
# http://localhost:8000
```

Absolutní cesty (`/brand/tokens.css`) fungují jen přes server, ne přes `file://`.

## Nasazení

Push do `main`. Pages vystaví do minuty.

## Self-hosting fontů

```bash
node scripts/build-fonts.js
```

Stáhne latin + latin-ext woff2 do `/fonts/` a vygeneruje `scripts/_fonts.css`.
Obsah pak patří do `<style>` v `index.html` místo `<link>` na Google Fonts.

## Grafický manuál

`/brand/` — živý dokument. Je shodný napříč všemi třemi weby; při změně palety nebo
komponent ho aktualizuj a propiš `tokens.css` do `feedco-web` a `ethel-web`.
