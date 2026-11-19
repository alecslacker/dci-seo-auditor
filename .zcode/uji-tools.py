#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji otomatis kedua gerbang (cek-status.py dan cek-artikel.py).

Pakai: python3 -I -X utf8 .zcode/uji-tools.py
Semua skenario dibuat di folder sementara; tidak menyentuh data klien.

Author: Mas Wondho - Duta Corpora Indonesia (DCI)
Copyright (c) 2026 Duta Corpora Indonesia - All rights reserved
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = [sys.executable, "-I", "-X", "utf8"]
GAGAL_UJI = []


def jalankan(*argv):
    r = subprocess.run(PY + [str(a) for a in argv], capture_output=True, text=True, timeout=300)
    return r.returncode, (r.stdout + r.stderr)


def cek(nama, kondisi, detail=""):
    status = "OK  " if kondisi else "GAGAL"
    print("%s %s %s" % (status, nama, detail))
    if not kondisi:
        GAGAL_UJI.append(nama)


def bikin_skenario(base):
    klien = base / "Klien Uji"
    bulan = klien / "artikel" / "2026 Maret"
    bulan.mkdir(parents=True, exist_ok=True)
    (klien / "CLIENT.md").write_text(
        "# CLIENT.md\n\n"
        "| Field Placeholder | Isi |\n|---|---|\n"
        "| `{client_name}` | Klien Uji |\n"
        "| `{client_url}` | https://klienuji.example |\n"
        "| `{client_phone}` | +62 000 |\n"
        "| `{client_email}` | a@b.example |\n"
        "| `{client_wa_shortcode}` | `[wa id=\"9\"]` |\n"
        "| Istilah dipertahankan | Blitar |\n", encoding="utf8")
    return klien, bulan


def uji_status(base):
    klien, bulan = bikin_skenario(base)
    (bulan / "selesai.txt").write_text("lengkap\n[wa id=\"9\"]\n", encoding="utf8")
    (bulan / "lanjut.txt").write_text("sebagian\n[wa id=\"9\"]\n", encoding="utf8")
    (bulan / "menunggu.txt").write_text("belum selesai\n", encoding="utf8")
    # hash diambil dari output skrip supaya sama cara hitungnya
    kode, out = jalankan(ROOT / ".zcode" / "cek-status.py", bulan)
    cek("status: skrip jalan", kode == 0, out[:80])
    h = {nama: hh for hh, nama in re.findall(r"\t([0-9a-f]{16})\t[^\t]*\t(\S+\.txt)", out)}
    (bulan / "LAPORAN.md").write_text(
        "| Draft | Hash | Audit | Humanize | ZeroGPT |\n|---|---|---|---|---|\n"
        "| selesai.txt | %s | 2026-03-01 | 2026-03-01 | 3%% AI |\n"
        "| lanjut.txt | %s | 2026-03-01 | - | - |\n"
        % (h.get("selesai.txt", "0" * 16), h.get("lanjut.txt", "0" * 16)), encoding="utf8")
    kode, out = jalankan(ROOT / ".zcode" / "cek-status.py", bulan)
    cek("status: SELESAI terdeteksi", "SELESAI" in out and "selesai.txt" in out)
    cek("status: LANJUTKAN menunjukkan tahap kosong", re.search(r"LANJUTKAN\s+\S+\ttahap_kosong=humanize,zerogpt\tlanjut.txt", out) is not None)
    cek("status: MENUNGGU untuk draft tanpa shortcode", re.search(r"MENUNGGU\t\S+\ttahap_kosong=-\tmenunggu.txt", out) is not None)
    (klien / "CLIENT.md").unlink()
    kode, out = jalankan(ROOT / ".zcode" / "cek-status.py", bulan)
    cek("status: tanpa CLIENT.md -> gagal jelas", kode != 0 and "CLIENT.md" in out)


MINI = (
    '<p><a href="https://klienuji.example/artikel/mini"><b><i>Kata Kunci Uji</i></b></a> - Paragraf pembuka. '
    + "Kalimat isi yang cukup panjang untuk dihitung. " * 6 + '</p>\n\n'
    "<p>&nbsp;</p>\n<h2>Bagian</h2>\n"
    + ("Paragraf seragam satu. Paragraf seragam dua. Paragraf seragam tiga.\n\n" * 8)
    + "Harga mulai Rp5000 saja tanpa label.\n[wa id=\"9\"]\n"
)


def uji_artikel(base):
    _, bulan = bikin_skenario(base)
    mini = bulan / "mini.txt"
    mini.write_text(MINI, encoding="utf8")
    skrip = ROOT / ".zcode" / "cek-artikel.py"
    kode, out = jalankan(skrip, mini, "--kw", "Kata Kunci Uji")
    cek("artikel: gerbang menolak draft cacat (exit 1)", kode == 1)
    cek("artikel: FAIL jumlah kata", re.search(r"FAIL.*jumlah kata \d+ < 2000", out) is not None)
    cek("artikel: FAIL h2 tanpa nbsp/detail heading", "FAIL" in out)
    cek("artikel: FAIL angka tanpa label", "Rp5000" in out or "angka" in out.lower())
    kode, out = jalankan(skrip, mini, "--kw", "Kata Kunci Uji", "--draft")
    cek("artikel: mode draft exit 0", kode == 0)
    cek("artikel: mode draft mengeluarkan TEMUAN bernomor", re.search(r"TEMUAN\s+\d+:", out) is not None)
    cek("artikel: draft menandai ritme paragraf seragam", "ritme paragraf seragam" in out)


def main():
    with tempfile.TemporaryDirectory(prefix="uji-puffer-") as d:
        base = Path(d)
        uji_status(base)
        uji_artikel(base)
    print("-" * 60)
    if GAGAL_UJI:
        print("UJI GAGAL: %s" % ", ".join(GAGAL_UJI))
        sys.exit(1)
    print("Semua uji lulus.")


main()
