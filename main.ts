import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry for news-image-20261119, v2 "Final Edition": "The World in One
// Day — Thursday 19 November 2026". The front page (entry.png, JPEG
// bytes under that name per RULES) is composed for this entry and shipped
// in the repo; this program copies it to the output directory. Same bytes
// every run: the file is only ever read, never modified or re-encoded.
// v2 rebuilds the page with the Final Edition treatment: every tile gets
// its own illustrated scene (hero, GTA, Gulf, Jeffries, Cyclone, EU),
// a denser seven-brief band, and a FINAL EDITION masthead chip.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
const bytes = readFileSync(join(here, "entry.png"));
// Guard the gate before writing: the file must be a whole JPEG
// (SOI marker FF D8 FF, EOI marker FF D9 at the end) and within the
// 1 MiB cap, so a corrupted, truncated or oversized asset fails loudly
// here instead of at grading time.
if (bytes.length < 4 || bytes[0] !== 0xff || bytes[1] !== 0xd8 || bytes[2] !== 0xff) {
  throw new Error("entry.png is not a JPEG (missing SOI marker)");
}
if (bytes[bytes.length - 2] !== 0xff || bytes[bytes.length - 1] !== 0xd9) {
  throw new Error("entry.png is not a whole JPEG (missing EOI marker)");
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
writeFileSync(join(outDir, "entry.png"), bytes);
