// Self-host brand fonty z npm balíčků @fontsource.
//
// Proč z npm a ne z fonts.googleapis.com: Google Fonts CDN je v EU sporný
// (přenos IP adres návštěvníků do USA) a v sandboxu bývá blokovaný.
// @fontsource publikuje ty samé soubory z Google Fonts repozitáře.
//
// Vstup:  node_modules/@fontsource/*
// Výstup: fonts/brand/*.woff2 + brand/fonts.css
//
// Spuštění:
//   npm install
//   node scripts/build-fonts.js

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'node_modules', '@fontsource');
const OUT_FONTS = path.join(ROOT, 'fonts', 'brand');
const OUT_CSS = path.join(ROOT, 'brand', 'fonts.css');

// Čeština potřebuje latin-ext (ě š č ř ž ů ď ť ň). Bez unicode-range by
// latin blok přebil latin-ext a diakritika by spadla na fallback font.
const SUBSETS = {
  latin:
    'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,' +
    'U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,' +
    'U+2212,U+2215,U+FEFF,U+FFFD',
  'latin-ext':
    'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,' +
    'U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,' +
    'U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF',
};

// Jen řezy, které web reálně používá. Přidávat jen s důvodem — každý řez
// je soubor navíc v repu.
const FACES = [
  { pkg: 'lora', family: 'Lora', weights: [400, 500, 600], italics: [500] },
  { pkg: 'dm-sans', family: 'DM Sans', weights: [400, 500, 700], italics: [400] },
  { pkg: 'dm-mono', family: 'DM Mono', weights: [400, 500], italics: [] },
  { pkg: 'space-grotesk', family: 'Space Grotesk', weights: [500, 700], italics: [] },
];

fs.rmSync(OUT_FONTS, { recursive: true, force: true });
fs.mkdirSync(OUT_FONTS, { recursive: true });

const blocks = [];
let copied = 0;

for (const face of FACES) {
  const variants = [
    ...face.weights.map((w) => ({ weight: w, style: 'normal' })),
    ...face.italics.map((w) => ({ weight: w, style: 'italic' })),
  ];

  for (const v of variants) {
    for (const [subset, range] of Object.entries(SUBSETS)) {
      const file = `${face.pkg}-${subset}-${v.weight}-${v.style}.woff2`;
      const src = path.join(SRC, face.pkg, 'files', file);
      if (!fs.existsSync(src)) {
        console.warn(`chybí: ${file}`);
        continue;
      }
      fs.copyFileSync(src, path.join(OUT_FONTS, file));
      copied++;
      blocks.push(
        `@font-face {\n` +
          `  font-family: '${face.family}';\n` +
          `  font-style: ${v.style};\n` +
          `  font-weight: ${v.weight};\n` +
          `  font-display: swap;\n` +
          `  src: url('/fonts/brand/${file}') format('woff2');\n` +
          `  unicode-range: ${range};\n` +
          `}`
      );
    }
  }
}

const header =
  `/* Vygenerováno scripts/build-fonts.js — needitovat ručně.\n` +
  `   Zdroj: npm @fontsource (soubory z Google Fonts).\n` +
  `   Přegenerovat: npm install && node scripts/build-fonts.js */\n\n`;

fs.mkdirSync(path.dirname(OUT_CSS), { recursive: true });
fs.writeFileSync(OUT_CSS, header + blocks.join('\n\n') + '\n', 'utf8');

console.log(`zkopírováno ${copied} souborů do fonts/brand/`);
console.log(`zapsáno ${path.relative(ROOT, OUT_CSS)} (${blocks.length} @font-face bloků)`);
