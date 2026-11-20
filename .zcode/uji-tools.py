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

    # Regresi: 'Anda' kapital sah di awal kalimat/paragraf, salah di tengah kalimat.
    anda = bulan / "anda.txt"
    anda.write_text(MINI + "\nAnda bisa menghubungi kami. Silakan hubungi sekarang. Anda siap?\n"
                    "Jika Anda butuh bantuan, kami siap.\n", encoding="utf8")
    kode, out = jalankan(skrip, anda, "--kw", "Kata Kunci Uji", "--draft")
    # Konteks temuan bisa memuat baris baru, jadi tangkap sampai TEMUAN/INFO/garis berikutnya.
    salah = re.findall(r"'Anda' kapital di tengah kalimat: (.*?)(?=\nTEMUAN|\nINFO|\n-{10})", out, re.S)
    cek("artikel: tepat 1 'Anda' salah ditandai (dari 3 kemunculan)", len(salah) == 1, "ditandai=%d" % len(salah))
    cek("artikel: yang ditandai adalah 'Jika Anda' di tengah kalimat", len(salah) == 1 and "Jika Anda" in salah[0], str(salah))

    # Regresi: draft tanpa anchor permalink tetap exit 0 (kontrak mode audit).
    polos = bulan / "polos.txt"
    polos.write_text("Draft polos tanpa anchor permalink.\n[wa id=\"9\"]\n", encoding="utf8")
    kode, out = jalankan(skrip, polos, "--draft")
    cek("artikel: draft tanpa anchor exit 0", kode == 0, "exit=%d" % kode)
    cek("artikel: draft tanpa anchor dilaporkan sebagai temuan", "anchor permalink" in out)
    kode, out = jalankan(skrip, polos)
    cek("artikel: gerbang final tanpa keyword tetap gagal (exit 2)", kode == 2, "exit=%d" % kode)


KW = "Kata Kunci Uji"
KALIMAT = [
    "Kegiatan rapat berjalan lancar dan para peserta menikmati hidangan yang tersaji dengan rapi.",
    "Panitia menyiapkan jadwal sejak pagi supaya setiap tamu mendapat giliran yang adil.",
    "Pengantaran dilakukan tepat waktu sehingga acara tidak tertunda oleh urusan konsumsi.",
    "Setiap menu dipilih dengan melihat selera peserta dan kebiasaan makan di daerah setempat.",
    "Pertanyaan yang paling sering muncul adalah soal jumlah porsi dan waktu pemesanan.",
    "Tim dapur memeriksa bahan sebelum dimasak agar rasa tetap terjaga sampai ke meja.",
    "Kemasan dibuat rapat sehingga makanan tetap hangat selama perjalanan menuju lokasi.",
    "Pemesan biasanya menghubungi kami beberapa hari sebelum kegiatan dimulai.",
]


def kalimat(n, mulai=0):
    return " ".join(KALIMAT[(mulai + i) % len(KALIMAT)] for i in range(n))


def artikel_lulus():
    """Artikel sintetis yang harus lolos gerbang final dengan 0 FAIL."""
    p1 = ('<p><a href="https://klienuji.example/artikel/lulus"><b><i>%s</i></b></a> - %s '
          '<a href="https://klienuji.example" target="_blank" rel="noopener"><b>Klien Uji</b></a> '
          'melayani wilayah <a href="https://id.wikipedia.org/wiki/Blitar" target="_blank" '
          'rel="noopener noreferrer">Blitar</a>.</p>' % (KW, kalimat(17)))
    gambar = ('<div style="border: 2px dashed #ff6600;">\n<strong>GAMBAR DISINI</strong><br> '
              '<em>Saran: foto hidangan tersaji di meja rapat\n</em><br> '
              '<small>Alt text: "%s - hidangan tersaji di meja rapat"</small>\n</div>' % KW)
    bagian = [p1, "<!--more-->", gambar]
    n_bold = 0
    for i in range(1, 8):
        judul = "Panduan %s Bagian %d" % (KW, i) if i <= 3 else "Catatan Pemesanan Bagian %d" % i
        bagian += ["<p>&nbsp;</p>", "<h2>%s</h2>" % judul]
        for j in range(4):
            if n_bold < 28:
                bagian.append("<p>%s <b>%s</b> %s</p>" % (kalimat(3, i + j), KW, kalimat(4, i + j + 3)))
                n_bold += 1
            else:
                bagian.append("<p>%s</p>" % kalimat(7, i + j))
        if i == 2:
            bagian.append("<ul>\n<li>Jadwal pengantaran</li>\n<li>Jumlah porsi</li>\n</ul>")
    bagian += ["<p>&nbsp;</p>", "<h2>Hubungi Kami Dari Kontak Resmi Klien Uji</h2>",
               "<b>WA:</b> +62 000\n<b>Telepon:</b> +62 000\n<b>Email:</b> a@b.example",
               "<p>Terima kasih sudah membaca sampai selesai.</p>", '[wa id="9"]']
    return "\n\n".join(bagian) + "\n"


def uji_artikel_lulus(base):
    _, bulan = bikin_skenario(base)
    skrip = ROOT / ".zcode" / "cek-artikel.py"
    lulus = bulan / "lulus.txt"
    lulus.write_text(artikel_lulus(), encoding="utf8")
    kode, out = jalankan(skrip, lulus)
    cek("lulus: artikel sehat 0 FAIL (exit 0)", kode == 0 and "0 FAIL" in out, out[-160:].replace("\n", " | "))

    # Mutasi: tiap perubahan kecil harus membuat gerbang menolak.
    isi = artikel_lulus()
    # (teks mutasi, potongan pesan FAIL yang wajib muncul)
    mutasi = {
        "ejaan tidak baku di awal kalimat": (isi.replace("<p>Terima kasih", "<p>Silahkan hubungi kami. Terima kasih"), "ejaan tidak baku: 'silahkan'"),
        "kata asing di awal kalimat": (isi.replace("<p>Terima kasih", "<p>Snack Box tersedia. Terima kasih"), "kata asing: 'snack'"),
        "more-tag hilang": (isi.replace("<!--more-->", ""), "<!--more--> ada 0"),
        "shortcode WA hilang": (isi.replace('\n\n[wa id="9"]', ""), "baris terakhir bukan shortcode"),
        "keyword body tidak dibold": (isi.replace("<b>%s</b>" % KW, KW, 1), "hanya"),
    }
    for nama, (teks, pesan) in mutasi.items():
        f = bulan / "mutasi.txt"
        f.write_text(teks, encoding="utf8")
        kode, out = jalankan(skrip, f)
        cek("lulus: mutasi '%s' ditolak" % nama, kode == 1 and pesan in out, "exit=%d" % kode)


class HalamanPalsu:
    def __init__(self, html_teks):
        self.html_teks = html_teks

    def read(self):
        return self.html_teks.encode("utf8")


def uji_kbbi():
    """kbbi_cek diuji dengan halaman palsu (tanpa jaringan)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("cek_artikel_uji", ROOT / ".zcode" / "cek-artikel.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    asli = modul.ureq.urlopen
    kasus = {
        "halaman kuota harian -> KUOTA (bukan dibaca sebagai kata)":
            ("<h2>Pencarian Anda telah mencapai batas maksimum dalam sehari</h2>", "KUOTA"),
        "entri tidak ditemukan -> TIDAK_ADA": ("<p>Entri tidak ditemukan</p>", "TIDAK_ADA"),
        "entri sah -> OK": ("<h2>kata</h2>", "OK"),
        "halaman tanpa h2 -> ERROR": ("<p>kosong</p>", "ERROR"),
    }
    try:
        for nama, (halaman, harap) in kasus.items():
            modul.ureq.urlopen = lambda *a, _h=halaman, **k: HalamanPalsu(_h)
            status, _ = modul.kbbi_cek("kata")
            cek("kbbi: " + nama, status == harap, "status=%s" % status)
    finally:
        modul.ureq.urlopen = asli


def main():
    with tempfile.TemporaryDirectory(prefix="uji-dci-seo-") as d:
        base = Path(d)
        uji_status(base)
        uji_artikel(base)
        uji_artikel_lulus(base)
    uji_kbbi()
    print("-" * 60)
    if GAGAL_UJI:
        print("UJI GAGAL: %s" % ", ".join(GAGAL_UJI))
        sys.exit(1)
    print("Semua uji lulus.")


main()
