# jakubsevela.cz — pravidla pro práci v tomhle repu

Statický web, žádný build. Hostuje GitHub Pages z branch `main`, root. Doména je v `CNAME`.

Tenhle soubor čte kdokoli, kdo v repu pracuje — Cowork, Claude Code i člověk.

## Co je kde

| Cesta | Co to je |
|-------|----------|
| `/` (`index.html`) | **Živý web.** Nový brand (dark-first, jantar), texty přenesené 1:1 ze staré verze. Tady se pracuje. |
| `/nahled/` | **Obsahová varianta v9** — jiné texty (hero „Pomáhám firmám získat z Heliosu maximum", sekce Služby, případové studie, FAQ, kontaktní formulář). `noindex` + robots disallow. Rozpracovaný návrh, ne živý web. |
| `/brand/` | Grafický manuál v1.1, `tokens.css` a `fonts.css` — zdroj pravdy vizuálního systému. |

Starý Bootstrap web z roku 2020 byl smazán 26. 7. 2026 (žije v git historii).
Spolu s ním `css/`, `js/`, `reference.html`, ikonové fonty a balast šablony v `images/`.

## Role webu

Hub v architektuře hub-and-spoke. `ethel.cz` a `feedco.cz` jsou samostatné weby (spokes),
prolinkované, nikoli podřízené. Hub je vizitka a důkaz kompetence — víc než jen výčet produktů.

Návštěvník = firma s Heliosem, která má problém. Do tří sekund musí potvrdit:
„tenhle člověk dělá Helios a vyřeší to, co potřebuju."

## Vizuální systém

Tokeny jsou v **`/brand/tokens.css`** — jediný zdroj pravdy pro barvy, typografii a radiusy.
Nikdy nepiš hexy natvrdo. Kompletní manuál je na `/brand/`.

- **Dark-first.** Pozadí `--bg` / `--bg-alt`, karty `--card`.
- **Accent = jantar `#dfa63e`.** Barva jen v akcentech (tečka, CTA, odkazy, ikony stavu),
  nikdy jako plocha na pozadí.
- **Buttony tónované:** 12 % podklad + 35 % border, text v light odstínu. Hover 18 % / 50 %.
  Plné barevné plochy jsou zakázané.
- **Typografie:** Lora (nadpisy) / DM Sans (text a UI) / DM Mono (detaily, kódy, labely) /
  Space Grotesk **jen** pro wordmark a monogram, nikde jinde.
- **Řezy nadpisů: čím větší, tím lehčí.** `h1`/`h2` v Lora **400** (`--weight-display`),
  `h3`/`h4` v **500** (`--weight-heading`). Nikdy nepiš váhu natvrdo. Velký nadpis
  v 600 konkuruje fotce i accentu — proto 400.
- **Šířka:** obsah v `--content-max` (1200 px). Hero je jediná sekce od kraje ke kraji;
  text v něm ale drží stejný `.wrap`, aby levá hrana lícovala se zbytkem stránky.
  Levou hranu hero fotky vázat na konec textového sloupce, ne na procento viewportu —
  jinak na širokém monitoru podjede text.
- **Wordmark:** `jakub<span class="dot">.</span>ševela`, malými písmeny.
  Tečka bold 700 + `font-size: 1.25em`. Univerzální pravidlo, bez výjimek.
- **Radius:** tlačítka 8 px, karty 12 px.
- **Kontrast:** text na tónované ploše vždy v `--accent-l` (drží AAA).
  `--text-2` nepoužívat pod 14 px.

### Když měníš tokeny

`brand/tokens.css` je shodný ve všech třech repech (`jakubsevela-web`, `feedco-web`,
`ethel-web`) — mění se jen accent blok. Změnu **propiš do ostatních dvou** a do manuálu
na `/brand/`. Jinak se weby začnou rozcházet, což je přesně to, čemu má systém zabránit.

## Fonty

Self-hostované v `fonts/brand/`, deklarace v `brand/fonts.css`. Žádné volání na
`fonts.googleapis.com` — v EU je to sporné (IP adresy návštěvníků odcházejí do USA)
a v sandboxu je to stejně blokované.

Přegenerování (jen když přibude nový řez):

```bash
npm install
node scripts/build-fonts.js
```

Skript bere soubory z npm balíčků `@fontsource/*` a generuje `@font-face` bloky
s `unicode-range` pro `latin` i `latin-ext`. **Latin-ext je pro češtinu povinný** —
bez `unicode-range` by latin blok přebil latin-ext a diakritika spadla na fallback.

Řezy, které se generují, jsou v konstantě `FACES` v `scripts/build-fonts.js`.
Přidávat jen s důvodem, každý řez je soubor navíc v repu.

## OG image

`og-image.png` (1200×630) se generuje ze šablony `scripts/og-image.html`:

```bash
npm install
node scripts/generate-og.js
```

Šablona je normální HTML v brandových tokenech — edituje se ona, ne PNG.
Tahá `/brand/fonts.css` absolutními cestami, takže ji nejde otevřít přes `file://`;
generátor si proto sám zvedne dočasný server nad rootem repa. Chrome se hledá
v `CHROME_PATH`, jinak na obvyklých místech (Linux i Windows).

Po přegenerování soubor commitni — Pages ho servíruje staticky.

## Texty

Česky, web je vykaný. Konkrétnost před přísliby: jména klientů, čísla, měřitelné výsledky.
Žádné „inovativní řešení na míru". Case studies drží formát **situace → řešení → výsledek**.
Nadpis H1 je o návštěvníkovi, ne o byznys modelu. Jména produktů do H1 nepatří.

## Co nedělat

- Nepřidávat závislosti a build krok do samotného webu. `npm` je tu jen pro generování
  fontů, nasazuje se čisté HTML. Cena statického webu je, že se nemůže rozbít.
- Nepoužívat `localStorage`/`sessionStorage`.
- Neměnit `CNAME` a nemazat `.nojekyll`. Bez `.nojekyll` Pages ignoruje soubory
  začínající podtržítkem.
- Nepřidávat PHP ani nic serverového — Pages umí jen statické soubory.
  Formuláře jdou přes Formspree (endpoint `xkgnqpnz` je v `/nahled/`).

## Známý technický dluh

- **Na živém webu není kontaktní formulář**, jen e-mail, telefon a LinkedIn.
  Formulář je připravený v `/nahled/` (Formspree `xkgnqpnz`) — čeká na doplnění.
- **`/nahled/` má portrét v hero jako base64 data URI** (~215 KB). Vytáhnout do souboru.
- **`/nahled/` tahá fonty z Google Fonts CDN.** Přepnout na `/brand/fonts.css` jako root.
- `programatorhelios.cz` je volný konec z roku 2020 — žije na jiné IP, k úklidu.
