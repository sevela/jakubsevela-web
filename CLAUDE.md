# jakubsevela.cz — pravidla pro práci v tomhle repu

Statický web, žádný build. Hostuje GitHub Pages z branch `main`, root. Doména je v `CNAME`.

Tenhle soubor čte kdokoli, kdo v repu pracuje — Cowork, Claude Code i člověk.

## ⚠ V repu jsou dva weby. Nepleť si je.

| Cesta | Co to je | Jak s tím zacházet |
|-------|----------|--------------------|
| `/` (`index.html`, `css/`, `js/`, `images/`, `fonts/`, `reference.html`) | **Starý web**, přenesený 1:1 z původního hostingu. Bootstrap šablona z roku 2020. | **Neinvestovat.** Je tu jen proto, aby přechod na Pages nezměnil nic navenek. Opravuj jen to, co je rozbité. |
| `/nahled/` | **Redesign (master v9)** v novém brandu. Sem jde veškerá práce na vzhledu a textech. | `noindex` + robots disallow. Až bude odladěný, přesune se na root a starý web se smaže. |
| `/brand/` | Grafický manuál v1.1 + `tokens.css` — zdroj pravdy vizuálního systému. | Platí pro `/nahled/`, ne pro starý web. |

**Když Jakub řekne „uprav web", myslí `/nahled/`.** Starý web se nepředělává, ten se zahodí.

## Role webu

Hub v architektuře hub-and-spoke. `ethel.cz` a `feedco.cz` jsou samostatné weby (spokes),
prolinkované, nikoli podřízené. Hub je vizitka a důkaz kompetence — víc než jen výčet produktů.

Návštěvník = firma s Heliosem, která má problém. Do tří sekund musí potvrdit:
„tenhle člověk dělá Helios a vyřeší to, co potřebuju."

## Vizuální systém (platí pro `/nahled/`)

Tokeny jsou v **`/brand/tokens.css`** — jediný zdroj pravdy pro barvy, typografii a radiusy.
Nikdy nepiš hexy natvrdo. Kompletní manuál je na `/brand/`.

- **Dark-first.** Pozadí `--bg` / `--bg-alt`, karty `--card`.
- **Accent = jantar `#dfa63e`.** Barva jen v akcentech (tečka, CTA, odkazy, ikony stavu),
  nikdy jako plocha na pozadí.
- **Buttony tónované:** 12 % podklad + 35 % border, text v light odstínu. Hover 18 % / 50 %.
  Plné barevné plochy jsou zakázané.
- **Typografie:** Lora (nadpisy) / DM Sans (text a UI) / DM Mono (detaily, kódy, labely) /
  Space Grotesk **jen** pro wordmark a monogram, nikde jinde.
- **Wordmark:** `jakub<span class="dot">.</span>ševela`, malými písmeny.
  Tečka bold 700 + `font-size: 1.25em`. Univerzální pravidlo, bez výjimek.
- **Radius:** tlačítka 8 px, karty 12 px.
- **Kontrast:** text na tónované ploše vždy v `--accent-l` (drží AAA).
  `--text-2` nepoužívat pod 14 px.

### Když měníš tokeny

`brand/tokens.css` je shodný ve všech třech repech (`jakubsevela-web`, `feedco-web`,
`ethel-web`) — mění se jen accent blok. Změnu **propiš do ostatních dvou** a do manuálu
na `/brand/`. Jinak se weby začnou rozcházet, což je přesně to, čemu má systém zabránit.

## Texty

Česky, web je vykaný. Konkrétnost před přísliby: jména klientů, čísla, měřitelné výsledky.
Žádné „inovativní řešení na míru". Case studies drží formát **situace → řešení → výsledek**.
Nadpis H1 je o návštěvníkovi, ne o byznys modelu. Jména produktů do H1 nepatří.

## Co nedělat

- Nepřidávat závislosti a build krok, dokud to nepůjde jinak. Cena statického webu je,
  že se nemůže rozbít.
- Nepoužívat `localStorage`/`sessionStorage`.
- Neměnit `CNAME` a nemazat `.nojekyll`. Bez `.nojekyll` Pages ignoruje soubory
  začínající podtržítkem.
- Nepřidávat PHP ani nic serverového — Pages umí jen statické soubory.
  Formuláře jdou přes Formspree (endpoint `xkgnqpnz` je v `/nahled/`).

## Známý technický dluh

### `/nahled/` (redesign)
- **Fonty jdou z Google Fonts CDN.** `ethel-web` je má self-hostované. Sjednotit:
  `node scripts/build-fonts.js` (potřebuje `fonts.googleapis.com` a `fonts.gstatic.com`),
  pak vygenerované `scripts/_fonts.css` vložit do `<style>` a odstranit `<link>` na Google.
  Pozor: `fonts/` teď obsahuje ikonové fonty starého webu, brand fonty přijdou vedle nich.
- **`og-image.png` neexistuje**, meta tagy na něj odkazují. `ethel-web` má generátor
  v `scripts/generate-og.js` — přenést.
- Portrét v hero je base64 data URI (~215 KB). Vytáhnout do souboru.
- Fotky referencí jsou v `/images/reference/` (obnoveny ze starého webu). Když fotka chybí,
  `onerror` ji odstraní a ukáže se iniciála z `data-initials` — stejně jako u referencí,
  které fotku nikdy neměly.
- Chybí blok „Jste můj zákazník, pokud…", který starý web má.

### starý web na rootu
- Kontaktní formulář je v `index.html` **zakomentovaný** — na původním hostingu už
  nefungoval (mířil na `sendmail.php`, to se nepřeneslo, na Pages by PHP neběželo).
- `reference.html` není odnikud odkazovaná, odkazuje na `https://www.jakubsevela.cz/`.
- V `images/` je ~150 souborů, z `index.html` se používá 18. Zbytek je balast šablony.
- Nepřeneseno z hostingu (schválně): `awstats/`, `.htaccess`, `.user.ini`, `sendmail.php`,
  `blank.html`. Starý `sitemap.xml` mířil na `programatorhelios.cz` — přepsán.
