# jakubsevela.cz — pravidla pro práci v tomhle repu

Statický web, žádný build. `index.html` je celá stránka (HTML + inline CSS + inline JS).
Hostuje GitHub Pages z branch `main`, root. Doména je v `CNAME`.

Tenhle soubor čte kdokoli, kdo v repu pracuje — Cowork, Claude Code i člověk.
**Když měníš vzhled, drž se pravidel níž.** Nejsou to preference, jsou to rozhodnutí.

## Role webu

Hub v architektuře hub-and-spoke. `ethel.cz` a `feedco.cz` jsou samostatné weby (spokes),
prolinkované, nikoli podřízené. Hub je vizitka a důkaz kompetence — víc než jen výčet produktů.

Návštěvník = firma s Heliosem, která má problém. Do tří sekund musí potvrdit:
„tenhle člověk dělá Helios a vyřeší to, co potřebuju."

## Vizuální systém

Tokeny jsou v **`/brand/tokens.css`** — jediný zdroj pravdy pro barvy, typografii a radiusy.
Nikdy nepiš hexy natvrdo do `index.html`. Kompletní manuál je na `/brand/`.

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

Česky, tykání v produktových textech se nepoužívá — web je vykaný.
Konkrétnost před přísliby: jména klientů, čísla, měřitelné výsledky. Žádné „inovativní řešení
na míru". Case studies drží formát **situace → řešení → výsledek**.

Nadpis H1 je o návštěvníkovi, ne o byznys modelu. Jména produktů do H1 nepatří.

## Co nedělat

- Nepřidávat závislosti a build krok, dokud to nepůjde jinak. Cena statického webu je,
  že se nemůže rozbít.
- Nepoužívat `localStorage`/`sessionStorage` — není potřeba a komplikuje.
- Neměnit `CNAME` a nemazat `.nojekyll`. Bez `.nojekyll` Pages ignoruje soubory
  začínající podtržítkem.
- Nesahat na `formspree.io` endpoint v kontaktním formuláři bez důvodu.

## Známý technický dluh

- **Fonty jdou z Google Fonts CDN.** `ethel-web` je má self-hostované v `/fonts/`.
  Sjednotit: `node scripts/build-fonts.js` (potřebuje přístup na `fonts.googleapis.com`
  a `fonts.gstatic.com`), pak vložit vygenerované `scripts/_fonts.css` do `<style>`
  a odstranit `<link>` na Google.
- **`og-image.png` neexistuje.** Meta tagy na něj odkazují. `ethel-web` má generátor
  v `scripts/generate-og.js` — přenést.
- **Fotky referencí** v `/images/reference/` chybí (zůstaly na původním hostingu).
  Do té doby se místo fotky zobrazí iniciály z `data-initials`.
- `index.html` má jeden portrét vložený jako base64 data URI (~215 KB). Vytáhnout do
  souboru, až na to přijde řeč.
