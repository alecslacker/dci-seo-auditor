#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DCI SEO Auditor - siapkan payload ZeroGPT untuk operator (manusia) yang akan memindai.

Aturan AGENT.md Section 6: pemindaian ZeroGPT dikerjakan operator, bukan agent.
Skrip ini hanya menyiapkan bahan pindai: strip HTML, buang blok editor/boilerplate,
batasi 15.000 karakter per bagian, lalu simpan sebagai payload-zerogpt.txt di folder
artikel yang sama.

Pakai (dari ROOT project):
  python -I -X utf8 alat/siap-zerogpt.py "klien/<Klien>/artikel/<YYYY Bulan>/<Slug> - Humanized.txt"

Keluaran: payload-zerogpt.txt (satu bagian bila muat, dua bila dipecah). Exit 0 sukses,
2 masukan tidak bisa diproses.

Author: Mas Wondho - Duta Corpora Indonesia (DCI)
Copyright (c) 2026 Duta Corpora Indonesia - All rights reserved
"""
import html
import re
import sys
from pathlib import Path

BATAS = 15000  # batas kolom gratis ZeroGPT (karakter)


def bersihkan(raw):
    """Teks murni tanpa blok editor, shortcode, kontak boilerplate, dan tag HTML."""
    t = re.sub(r"<div.*?</div>", " ", raw, flags=re.S)      # blok GAMBAR DISINI
    t = re.sub(r"<!--more-->", " ", t)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = "\n".join(b for b in t.split("\n")
                  if "whatsapp_button" not in b and "Alt text:" not in b)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip()


def pecah(teks):
    """Pecah di batas kalimat bila melewati batas karakter."""
    if len(teks) <= BATAS:
        return [teks]
    bagian, n = [], 0
    for kalimat in re.findall(r"[^.!?]+[.!?]+|\S+$", teks):
        if n + len(kalimat) > BATAS and bagian:
            bagian.append(kalimat.strip())
            n = len(kalimat)
        else:
            bagian.append((bagian.pop() + " " if bagian else "") + kalimat.strip())
            n = len(bagian[-1])
    return [b.strip() for b in bagian if b.strip()]


def main():
    if len(sys.argv) != 2:
        print("Pakai: python -I -X utf8 alat/siap-zerogpt.py \"<artikel - Humanized.txt>\"")
        sys.exit(2)
    p = Path(sys.argv[1])
    if not p.is_file():
        print("GAGAL: berkas '%s' tidak ada." % p)
        sys.exit(2)
    try:
        raw = p.read_text(encoding="utf8")
    except UnicodeDecodeError as e:
        print("GAGAL: '%s' bukan UTF-8 (byte tidak sah di posisi %d)." % (p.name, e.start))
        sys.exit(2)
    bagian = pecah(bersihkan(raw))
    if not bagian:
        print("GAGAL: artikel kosong.")
        sys.exit(2)
    out = p.parent / "payload-zerogpt.txt"
    isi = []
    for i, b in enumerate(bagian, 1):
        label = ("BAGIAN %d/%d\n\n" % (i, len(bagian))) if len(bagian) > 1 else ""
        isi.append(label + b)
    out.write_text(("\n\n=====\n\n").join(isi) + "\n", encoding="utf8")
    print("OK: %s (%d bagian, karakter terpanjang %d)" % (out, len(bagian), max(len(b) for b in bagian)))
    print()
    print("=" * 60)
    print("TUGAS OPERATOR (manusia) — ikuti langkah berikut:")
    print("=" * 60)
    print("1. Buka https://www.zerogpt.com/ di browser.")
    print("2. Buka berkas: %s" % out)
    if len(bagian) > 1:
        print("3. Tempel isi BAGIAN 1/%d (sebelum baris =====) ke kolom teks," % len(bagian))
        print("   klik \"Detect Text\", tunggu 15-30 detik, catat hasilnya.")
        print("4. Ulangi untuk tiap bagian berikutnya (BAGIAN 2/%d, dst)." % len(bagian))
        print("5. Laporkan ke agent: verdict + AI % tiap bagian, contoh:")
        print("   \"Bagian 1: Human written, AI 3,8%. Bagian 2: Human written, AI 4,1%.\"")
    else:
        print("3. Tempel seluruh isi berkas itu ke kolom teks, klik \"Detect Text\",")
        print("   tunggu 15-30 detik, catat hasilnya.")
        print("4. Laporkan ke agent: verdict + AI %, contoh:")
        print("   \"Human written, AI 3,8%.\"")
    print()
    print("Sebelum operator melapor, kolom ZeroGPT diisi MENUNGGU OPERATOR")
    print("dan artikel belum boleh dinyatakan final.")


if __name__ == "__main__":
    main()
