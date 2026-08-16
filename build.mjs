import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join, normalize, resolve } from "node:path";
import { gunzipSync } from "node:zlib";

const root = resolve(process.cwd());
const output = join(root, "dist");
const archive = gunzipSync(readFileSync(join(root, "site.tar.gz")));

if (existsSync(output)) rmSync(output, { recursive: true, force: true });
mkdirSync(output, { recursive: true });

function text(start, length) {
  const end = start + length;
  return archive.subarray(start, end).toString("utf8").replace(/\0.*$/s, "").trim();
}

let offset = 0;
let files = 0;
while (offset + 512 <= archive.length) {
  const header = archive.subarray(offset, offset + 512);
  if (header.every((byte) => byte === 0)) break;

  const name = text(offset, 100);
  const sizeText = text(offset + 124, 12).replace(/[^0-7]/g, "");
  const size = sizeText ? Number.parseInt(sizeText, 8) : 0;
  const type = String.fromCharCode(archive[offset + 156] || 48);
  const prefix = text(offset + 345, 155);
  const relative = normalize(prefix ? `${prefix}/${name}` : name).replace(/^([/\\])+/, "");
  const target = resolve(output, relative);

  if (!target.startsWith(`${output}/`) && target !== output) throw new Error(`Unsafe archive path: ${relative}`);
  if (type === "5") {
    mkdirSync(target, { recursive: true });
  } else if (type === "0" || type === "\0") {
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, archive.subarray(offset + 512, offset + 512 + size));
    files += 1;
  }
  offset += 512 + Math.ceil(size / 512) * 512;
}

if (!existsSync(join(output, "index.html")) || files < 10) {
  throw new Error("Static bundle extraction failed");
}
console.log(`Vitória static bundle prepared: ${files} files.`);
