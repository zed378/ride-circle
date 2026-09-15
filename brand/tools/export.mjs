// usage: node export.mjs jobs.json   — jobs: [{src, out, width, height?}]
import { Resvg } from '@resvg/resvg-js';
import fs from 'node:fs';
import path from 'node:path';

const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
for (const job of jobs) {
  const svg = fs.readFileSync(job.src, 'utf8');
  const r = new Resvg(svg, {
    fitTo: { mode: 'width', value: job.width },
    font: { loadSystemFonts: true, defaultFontFamily: 'Arial' },
  });
  fs.mkdirSync(path.dirname(job.out), { recursive: true });
  fs.writeFileSync(job.out, r.render().asPng());
}
console.log(`rendered ${jobs.length} png`);
