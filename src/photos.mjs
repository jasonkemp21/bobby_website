// One-off image pipeline for the logo variants and the share image. Run: node src/photos.mjs
// Job photos are handled by src/jobphotos.py.
import { createRequire } from 'module';
import path from 'path';
import { fileURLToPath } from 'url';
const require = createRequire(import.meta.url);
let sharp; try { sharp = require('sharp'); } catch { sharp = require('/opt/npm-tools/node_modules/sharp'); }
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const OUT = path.join(ROOT, 'img');
const LOGO = path.join(ROOT, 'assets/logo/ks-logo-trimmed.png');

// Logo for the white header, and a light version (black lettering turned white) for the dark footer.
await sharp(LOGO).resize({ width: 520 }).webp({ quality: 92, alphaQuality: 100 }).toFile(path.join(OUT, 'ks-logo.webp'));
{
  const { data, info } = await sharp(LOGO).resize({ width: 520 }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  for (let i = 0; i < data.length; i += 4) {
    const [r, g, b] = [data[i], data[i + 1], data[i + 2]];
    if (r < 110 && g < 110 && b < 110) { data[i] = 255; data[i + 1] = 255; data[i + 2] = 255; }
  }
  await sharp(data, { raw: info }).webp({ quality: 92, alphaQuality: 100 }).toFile(path.join(OUT, 'ks-logo-light.webp'));
}
// Share image: logo on white, 1200x630.
{
  const logo = await sharp(LOGO).resize({ width: 760 }).toBuffer();
  await sharp({ create: { width: 1200, height: 630, channels: 3, background: '#ffffff' } }).composite([{ input: logo, gravity: 'centre' }]).jpeg({ quality: 88 }).toFile(path.join(OUT, 'share.jpg'));
}
