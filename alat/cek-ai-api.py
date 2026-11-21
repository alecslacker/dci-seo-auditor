#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DCI SEO Auditor - detektor AI per kalimat lewat Winston AI (tambahan, bukan pengganti ZeroGPT).

Tujuan: agent tahu KALIMAT MANA yang dinilai terdengar AI, lalu merevisinya.
Skor Winston adalah skor MANUSIA 0-100 (tinggi = manusiawi), kebalikan ZeroGPT.
Hasil ini indikatif: detektor berbeda tidak selalu sependapat, dan teks manusia yang
berupa langkah resep atau daftar bisa dinilai rendah. Gerbang akhir tetap ZeroGPT
oleh operator sampai ambang dikalibrasi.

Kunci API TIDAK disimpan di repo. Set lewat variabel lingkungan WINSTON_API_KEY:
  Windows (PowerShell): $env:WINSTON_API_KEY = "<kunci>"
  macOS/Linux:          export WINSTON_API_KEY="<kunci>"

Pakai (dari ROOT project):
  python -I -X utf8 alat/cek-ai-api.py "klien/<Klien>/artikel/<YYYY Bulan>/<Slug> - Humanized.txt" [--ambang 50]

Biaya: 1 kredit per kata. Satu artikel 1.000 kata = 1.000 kredit. Cek sisa kredit di keluaran.
Keluaran: kalimat-ai.txt di folder artikel. Exit 0 selesai, 2 masukan atau API bermasalah.

Author: Duta Corpora Indonesia (DCI)
Copyright (c) 2026 Duta Corpora Indonesia - All rights reserved
"""
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

URL = os.environ.get("DCI_AI_API_URL", "https://api.gowinston.ai/v2/ai-content-detection")
MIN_KARAKTER = 300       # batas bawah API
MAKS_KARAKTER = 100000   # di bawah batas API 150.000, pecah di batas kalimat
AMBANG_AWAL = 50.0       # kalimat dengan skor manusia di bawah ini ditandai
ULANG_MAKS = 2           # ulangi hanya untuk 429/500/503

PESAN = {
    400: "Permintaan ditolak API (teks atau parameter tidak sah).",
    401: "Kunci API salah atau sudah dicabut. Periksa WINSTON_API_KEY.",
    402: "Kredit Winston habis. Tambah kredit di dashboard dev.gowinston.ai.",
    403: "Akses ditolak API.",
    415: "Format permintaan tidak didukung API.",
    429: "Terlalu banyak permintaan. Coba lagi beberapa menit lagi.",
    500: "Server Winston bermasalah. Coba lagi nanti.",
    503: "Layanan Winston sedang tidak tersedia. Coba lagi nanti.",
}


def url_sah(url):
    """Kunci API hanya boleh dikirim ke Winston (https) atau server tiruan lokal untuk uji."""
    p = urllib.parse.urlparse(url)
    if p.scheme == "https" and (p.hostname or "") in ("api.gowinston.ai", "gowinston.ai"):
        return True
    return p.scheme == "http" and (p.hostname or "") in ("127.0.0.1", "localhost")


def muat_bersihkan():
    """Pakai ulang pembersih teks dari siap-zerogpt.py agar hasil konsisten."""
    spec = importlib.util.spec_from_file_location("siap_zerogpt", Path(__file__).with_name("siap-zerogpt.py"))
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul.bersihkan


def pecah(teks, maks=MAKS_KARAKTER):
    """Pecah di batas kalimat bila teks melewati batas karakter API."""
    if len(teks) <= maks:
        return [teks]
    bagian, kini = [], ""
    for kalimat in re.findall(r"[^.!?]+[.!?]+|\S+$", teks):
        if kini and len(kini) + len(kalimat) > maks:
            bagian.append(kini.strip())
            kini = ""
        kini += kalimat
    if kini.strip():
        bagian.append(kini.strip())
    return bagian


def panggil(teks, kunci):
    """Satu panggilan Winston. Mengembalikan dict JSON, atau melempar RuntimeError berpesan jelas."""
    if not url_sah(URL):
        raise RuntimeError("DCI_AI_API_URL ditolak: kunci hanya boleh dikirim ke api.gowinston.ai atau 127.0.0.1.")
    badan = json.dumps({"text": teks, "language": "id", "sentences": True}).encode("utf8")
    for percobaan in range(ULANG_MAKS + 1):
        req = urllib.request.Request(URL, data=badan, method="POST", headers={
            "Authorization": "Bearer " + kunci,
            "Content-Type": "application/json",
            "User-Agent": "dci-seo-auditor/1.0",
        })
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and percobaan < ULANG_MAKS:
                time.sleep(2 * (percobaan + 1))
                continue
            raise RuntimeError("HTTP %d. %s" % (e.code, PESAN.get(e.code, "Kesalahan tak dikenal dari API."))) from None
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if percobaan < ULANG_MAKS:
                time.sleep(2 * (percobaan + 1))
                continue
            raise RuntimeError("Tidak bisa menghubungi API (%s). Periksa koneksi internet." % e) from None
        except ValueError:
            raise RuntimeError("Balasan API bukan JSON yang sah.") from None
    raise RuntimeError("Gagal setelah beberapa percobaan.")


def parse_argumen(argv):
    ambang, sisa, i = AMBANG_AWAL, [], 1
    while i < len(argv):
        if argv[i] == "--ambang":
            if i + 1 >= len(argv):
                return None, None
            try:
                ambang = float(argv[i + 1].replace(",", "."))
            except ValueError:
                return None, None
            i += 2
        else:
            sisa.append(argv[i])
            i += 1
    if len(sisa) != 1 or not 0 < ambang <= 100:
        return None, None
    return sisa[0], ambang


def main():
    path, ambang = parse_argumen(sys.argv)
    if path is None:
        print("Pakai: python -I -X utf8 alat/cek-ai-api.py \"<artikel - Humanized.txt>\" [--ambang 50]")
        sys.exit(2)
    kunci = os.environ.get("WINSTON_API_KEY", "").strip()
    if not kunci:
        print("GAGAL: variabel lingkungan WINSTON_API_KEY belum diisi.")
        print("Windows (PowerShell): $env:WINSTON_API_KEY = \"<kunci>\"   lalu jalankan ulang di jendela yang sama.")
        print("Kunci tidak boleh ditulis ke berkas repo.")
        sys.exit(2)
    p = Path(path)
    if not p.is_file():
        print("GAGAL: berkas '%s' tidak ada." % p)
        sys.exit(2)
    try:
        raw = p.read_text(encoding="utf8")
    except UnicodeDecodeError as e:
        print("GAGAL: '%s' bukan UTF-8 (byte tidak sah di posisi %d)." % (p.name, e.start))
        sys.exit(2)
    teks = muat_bersihkan()(raw)
    if len(teks) < MIN_KARAKTER:
        print("GAGAL: teks bersih hanya %d karakter; API butuh minimal %d." % (len(teks), MIN_KARAKTER))
        sys.exit(2)

    skor_bagian, kalimat_semua, sisa_kredit, bobot = [], [], None, []
    for bag in pecah(teks):
        try:
            hasil = panggil(bag, kunci)
        except RuntimeError as e:
            print("GAGAL: %s" % e)
            sys.exit(2)
        if "score" not in hasil:
            print("GAGAL: balasan API tidak memuat skor (%s)." % str(hasil.get("error", "tanpa keterangan"))[:120])
            sys.exit(2)
        skor_bagian.append(float(hasil["score"]))
        bobot.append(len(bag))
        kalimat_semua.extend(hasil.get("sentences") or [])
        sisa_kredit = hasil.get("credits_remaining", sisa_kredit)
        serangan = hasil.get("attack_detected")
        if isinstance(serangan, dict):
            serangan = [k for k, v in serangan.items() if v]
        if serangan:
            print("PERINGATAN: API mendeteksi karakter tersembunyi: %s" % serangan)

    skor = sum(s * b for s, b in zip(skor_bagian, bobot)) / sum(bobot)
    ditandai = [(n, float(k.get("score", 100)), k.get("text", "").strip())
                for n, k in enumerate(kalimat_semua, 1) if float(k.get("score", 100)) < ambang]
    ditandai.sort(key=lambda x: x[1])

    baris = [
        "Detektor: Winston AI (bahasa id). Skor = skor MANUSIA 0-100, tinggi = manusiawi.",
        "Indikatif, BUKAN ZeroGPT. Teks prosedural (langkah resep, daftar) bisa dinilai rendah padahal ditulis manusia.",
        "Skor keseluruhan: %.1f manusia | kalimat dinilai: %d | ditandai (< %g): %d"
        % (skor, len(kalimat_semua), ambang, len(ditandai)),
        "",
    ]
    if ditandai:
        baris.append("KALIMAT DITANDAI (skor terendah dulu). Tulis ulang dengan ritme dan kata kerja berbeda, jangan ubah fakta:")
        for n, s, t in ditandai:
            baris.append("[%d] %.1f | %s" % (n, s, t))
    else:
        baris.append("Tidak ada kalimat di bawah ambang.")
    out = p.parent / "kalimat-ai.txt"
    out.write_text("\n".join(baris) + "\n", encoding="utf8")

    print("OK: %s" % out)
    print("Skor Winston: %.1f manusia | ditandai: %d dari %d kalimat (ambang < %g)"
          % (skor, len(ditandai), len(kalimat_semua), ambang))
    if sisa_kredit is not None:
        print("Kredit tersisa: %s" % sisa_kredit)
    print("Catatan: ini pembanding Winston, bukan hasil ZeroGPT. Gerbang akhir tetap ZeroGPT oleh operator.")


if __name__ == "__main__":
    main()
