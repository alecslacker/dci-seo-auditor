"""Gerbang sebelum audit: klasifikasi tiap draft di folder bulan klien.

Pakai: python3 -I .zcode/cek-status.py "klien/<Klien>/artikel/<YYYY Bulan>"
Sumber status: tabel ledger di LAPORAN.md folder bulan (lihat AGENT.md Section 7).
Hanya membaca, tidak pernah menulis.

Author: Mas Wondho - Duta Corpora Indonesia (DCI)
Copyright (c) 2026 Duta Corpora Indonesia - All rights reserved
"""
import hashlib
import re
import sys
from pathlib import Path

SUFFIX = " - Humanized"
# Berkas pendamping, bukan draft: hasil akhir dan berkas meta (judul SEO, deskripsi meta, slug).
ABAIKAN = (SUFFIX, " - Meta")


def sidik(path):
    # Normalisasi supaya CRLF/LF dan spasi akhir baris tidak mengubah sidik jari.
    baris = [b.rstrip() for b in path.read_text(encoding="utf-8").splitlines()]
    isi = "\n".join(b for b in baris if b)
    return hashlib.sha256(isi.encode("utf-8")).hexdigest()[:16], isi


def baca_shortcode(folder_bulan):
    client = folder_bulan.parent.parent / "CLIENT.md"
    if not client.exists():
        sys.exit(f"GAGAL: {client} tidak ada. Isi CLIENT.md dulu.")
    m = re.search(r"\{client_wa_shortcode\}`\s*\|\s*`([^`]+)`", client.read_text(encoding="utf-8"))
    if not m:
        sys.exit("GAGAL: field {client_wa_shortcode} di CLIENT.md kosong atau tidak terbaca.")
    return m.group(1).strip()


def baca_ledger(laporan):
    baris_ledger = {}
    if not laporan.exists():
        return baris_ledger
    for b in laporan.read_text(encoding="utf-8").splitlines():
        sel = [s.strip() for s in b.strip().strip("|").split("|")]
        if len(sel) >= 5 and re.fullmatch(r"[0-9a-f]{16}", sel[1]):
            baris_ledger[sel[0]] = {"hash": sel[1], "audit": sel[2], "humanize": sel[3], "zerogpt": sel[4]}
    return baris_ledger


def main(argv):
    if len(argv) != 2:
        sys.exit(__doc__)
    folder = Path(argv[1])
    if not folder.is_dir():
        sys.exit(f"GAGAL: folder {folder} tidak ada.")
    shortcode = baca_shortcode(folder)
    ledger = baca_ledger(folder / "LAPORAN.md")

    for f in sorted(folder.glob("*.txt")):
        if f.stem.endswith(ABAIKAN):
            continue
        h, isi = sidik(f)
        ada_humanized = (folder / f"{f.stem}{SUFFIX}.txt").exists()
        lengkap = isi.splitlines()[-1].strip() == shortcode if isi else False
        row = ledger.get(f.name)
        if row is None:
            status = "TANPA-CATATAN" if ada_humanized else ("BARU" if lengkap else "MENUNGGU")
            kosong = "-"
        elif row["hash"] != h:
            status, kosong = "BERUBAH", "-"
        else:
            tahap = [k for k in ("audit", "humanize", "zerogpt") if row[k] in ("", "-")]
            status = "LANJUTKAN" if tahap else "SELESAI"
            kosong = ",".join(tahap) or "-"
        print(f"{status}\t{h}\ttahap_kosong={kosong}\t{f.name}")


main(sys.argv)
