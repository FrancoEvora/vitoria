import { createHash } from "node:crypto";
import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, normalize, resolve, sep } from "node:path";
import { gunzipSync } from "node:zlib";

const root = resolve(process.cwd());
const output = join(root, "dist");
const partDirectory = join(root, "bundle");
const expectedPartCount = 7;
const expectedCompressedBytes = 31_432;
const expectedSha256 = "fc79600319a3412aeb532ead625e3af1f231c3ea37703d20af3308af0829346e";

const parts = readdirSync(partDirectory)
  .filter((name) => /^part-\d{3}\.txt$/.test(name))
  .sort();

if (parts.length !== expectedPartCount) {
  throw new Error(`Static bundle parts missing: expected ${expectedPartCount}, found ${parts.length}`);
}

const encoded = parts
  .map((name) => readFileSync(join(partDirectory, name), "utf8").trim())
  .join("");
const compressed = Buffer.from(encoded, "base64");
const compressedSha256 = createHash("sha256").update(compressed).digest("hex");

if (compressed.length !== expectedCompressedBytes) {
  throw new Error(`Static bundle size mismatch: expected ${expectedCompressedBytes}, found ${compressed.length}`);
}
if (compressedSha256 !== expectedSha256) {
  throw new Error(`Static bundle checksum mismatch: expected ${expectedSha256}, found ${compressedSha256}`);
}

const archive = gunzipSync(compressed);
if (existsSync(output)) rmSync(output, { recursive: true, force: true });
mkdirSync(output, { recursive: true });

function readText(start, length) {
  return archive
    .subarray(start, start + length)
    .toString("utf8")
    .replace(/\0.*$/s, "")
    .trim();
}

let offset = 0;
let fileCount = 0;
while (offset + 512 <= archive.length) {
  const header = archive.subarray(offset, offset + 512);
  if (header.every((byte) => byte === 0)) break;

  const name = readText(offset, 100);
  const sizeText = readText(offset + 124, 12).replace(/[^0-7]/g, "");
  const size = sizeText ? Number.parseInt(sizeText, 8) : 0;
  const type = String.fromCharCode(archive[offset + 156] || 48);
  const prefix = readText(offset + 345, 155);
  const relative = normalize(prefix ? `${prefix}/${name}` : name).replace(/^([/\\])+/, "");
  const target = resolve(output, relative);
  const outputPrefix = output.endsWith(sep) ? output : `${output}${sep}`;

  if (!target.startsWith(outputPrefix) && target !== output) {
    throw new Error(`Unsafe archive path: ${relative}`);
  }

  if (type === "5") {
    mkdirSync(target, { recursive: true });
  } else if (type === "0" || type === "\0") {
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, archive.subarray(offset + 512, offset + 512 + size));
    fileCount += 1;
  }

  offset += 512 + Math.ceil(size / 512) * 512;
}

if (!existsSync(join(output, "index.html")) || !existsSync(join(output, "admin.html")) || fileCount < 10) {
  throw new Error(`Static bundle extraction failed: ${fileCount} files`);
}

console.log(`Vitória static bundle prepared: ${fileCount} files, sha256 ${compressedSha256}.`);
