# jakubsevela.cz

Osobní web Jakuba Ševely — specialista na Helios iNuvio. Hub v architektuře hub-and-spoke;
produktové weby [ethel.cz](https://ethel.cz) a [feedco.cz](https://feedco.cz) stojí samostatně.

Statický web bez buildu. Nasazuje GitHub Pages z branch `main`, root.

```
index.html            živý web — nový brand, texty přenesené 1:1 ze staré verze
og-image.png          náhledový obrázek pro sdílení, generovaný
images/               fotky referencí, loga klientů, favicon
fonts/brand/          self-hostované woff2 (Lora, DM Sans, DM Mono, Space Grotesk)

nahled/index.html     obsahová varianta v9 — jiné texty, noindex
brand/
  tokens.css          zdroj pravdy pro barvy, typografii, radiusy
  fonts.css           @font-face deklarace, generované
  index.html          grafický manuál v1.1
scripts/
  build-fonts.js      generuje fonts/brand/ + brand/fonts.css z npm @fontsource
  generate-og.js      generuje og-image.png ze scripts/og-image.html
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

## Nasazení

Push do `main`. Pages vystaví do minuty.

## Fonty

```bash
npm install
node scripts/build-fonts.js
```

Spouštět jen když přibude nový řez písma. Detaily v `CLAUDE.md`.

## Grafický manuál

`/brand/` — živý dokument. Je shodný napříč všemi třemi weby; při změně palety nebo
komponent ho aktualizuj a propiš `tokens.css` do `feedco-web` a `ethel-web`.
