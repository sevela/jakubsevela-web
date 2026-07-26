# jakubsevela.cz

Osobní web Jakuba Ševely — specialista na Helios iNuvio. Hub v architektuře hub-and-spoke;
produktové weby [ethel.cz](https://ethel.cz) a [feedco.cz](https://feedco.cz) stojí samostatně.

Statický web bez buildu. Nasazuje GitHub Pages z branch `main`, root.

V repu jsou dva weby vedle sebe:

```
index.html            STARÝ web, přenesený 1:1 z původního hostingu (bootstrap šablona)
css/ js/ images/      jeho assety
reference.html        orphan stránka starého webu, není odnikud odkazovaná
fonts/                ikonové fonty starého webu (FontAwesome, Themify, Linearicons)

nahled/index.html     REDESIGN (master v9) v novém brandu — noindex, sem jde veškerá práce
brand/
  tokens.css          zdroj pravdy pro barvy, typografii, radiusy
  index.html          grafický manuál v1.1
scripts/
  build-fonts.js      self-hosting Google Fonts do /fonts/
CNAME                 jakubsevela.cz
.nojekyll             vypíná Jekyll — bez toho Pages ignoruje soubory s podtržítkem
robots.txt            zakazuje /brand/ a /nahled/
sitemap.xml
CLAUDE.md             pravidla pro práci v repu — přečti dřív než začneš
```

## Lokální náhled

```bash
python3 -m http.server 8000
# http://localhost:8000
```

Absolutní cesty (`/brand/tokens.css`) fungují jen přes server, ne přes `file://`.
Redesign je na `http://localhost:8000/nahled/`.

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
