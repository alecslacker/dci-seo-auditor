#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji otomatis kedua gerbang (cek-status.py dan cek-artikel.py).

Pakai: python3 -I -X utf8 alat/uji-tools.py
Semua skenario dibuat di folder sementara; tidak menyentuh data klien.

Author: Mas Wondho - Duta Corpora Indonesia (DCI)
Copyright (c) 2026 Duta Corpora Indonesia - All rights reserved
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = [sys.executable, "-I", "-X", "utf8"]
GAGAL_UJI = []
JUMLAH_UJI = [0]


def jalankan(*argv):
    r = subprocess.run(PY + [str(a) for a in argv], capture_output=True, text=True, timeout=300)
    return r.returncode, (r.stdout + r.stderr)


def cek(nama, kondisi, detail=""):
    JUMLAH_UJI[0] += 1
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
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("status: skrip jalan", kode == 0, out[:80])
    h = {nama: hh for hh, nama in re.findall(r"\t([0-9a-f]{16})\t[^\t]*\t(\S+\.txt)", out)}
    (bulan / "LAPORAN.md").write_text(
        "| Draft | Hash | Audit | Humanize | ZeroGPT |\n|---|---|---|---|---|\n"
        "| selesai.txt | %s | 2026-03-01 | 2026-03-01 | 3%% AI |\n"
        "| lanjut.txt | %s | 2026-03-01 | - | - |\n"
        % (h.get("selesai.txt", "0" * 16), h.get("lanjut.txt", "0" * 16)), encoding="utf8")
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("status: SELESAI terdeteksi", "SELESAI" in out and "selesai.txt" in out)
    cek("status: LANJUTKAN menunjukkan tahap kosong", re.search(r"LANJUTKAN\s+\S+\ttahap_kosong=humanize,zerogpt\tlanjut.txt", out) is not None)
    cek("status: MENUNGGU untuk draft tanpa shortcode", re.search(r"MENUNGGU\t\S+\ttahap_kosong=-\tmenunggu.txt", out) is not None)
    (klien / "CLIENT.md").unlink()
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
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
    skrip = ROOT / "alat" / "cek-artikel.py"
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
    p1 = ('<p><a href="https://klienuji.example/artikel/kata-kunci-uji"><b><i>%s</i></b></a> - %s '
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
    skrip = ROOT / "alat" / "cek-artikel.py"
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


META_BAIK = ("Judul SEO: Kata Kunci Uji | Klien Uji\n"
             "Deskripsi meta: Kata Kunci Uji untuk kebutuhan rapat dan acara kantor di Blitar.\n"
             "Slug: kata-kunci-uji\n")


def uji_meta(base):
    _, bulan = bikin_skenario(base)
    skrip = ROOT / "alat" / "cek-artikel.py"
    art = bulan / "lulus - Humanized.txt"
    art.write_text(artikel_lulus(), encoding="utf8")
    meta = bulan / "lulus - Meta.txt"                       # nama dasar = nama artikel tanpa " - Humanized"

    kode, out = jalankan(skrip, art)
    cek("meta: tanpa berkas meta hanya WARN, bukan FAIL", kode == 0 and "berkas meta" in out, "exit=%d" % kode)

    meta.write_text(META_BAIK, encoding="utf8")
    kode, out = jalankan(skrip, art)
    cek("meta: berkas meta benar lolos 0 FAIL", kode == 0 and "0 FAIL" in out, out[-120:].replace("\n", " | "))

    kasus = {
        "judul SEO tanpa keyword": (META_BAIK.replace("Judul SEO: Kata Kunci Uji", "Judul SEO: Judul Lain"), "judul SEO tidak memuat keyword"),
        "deskripsi tanpa keyword": (META_BAIK.replace("Deskripsi meta: Kata Kunci Uji untuk", "Deskripsi meta: Layanan untuk"), "deskripsi meta tidak memuat keyword"),
        "slug tanpa keyword": (META_BAIK.replace("Slug: kata-kunci-uji", "Slug: nama-lain"), "tidak memuat keyword"),
        "slug berbeda dari anchor": (META_BAIK.replace("Slug: kata-kunci-uji", "Slug: kata-kunci-uji-lengkap"), "berbeda dari slug di anchor"),
        "slug berhuruf besar": (META_BAIK.replace("Slug: kata-kunci-uji", "Slug: Kata-Kunci-Uji"), "bukan huruf kecil"),
        "field kosong": (META_BAIK.replace("Slug: kata-kunci-uji", "Slug:"), "field 'slug' kosong"),
    }
    for nama, (teks, pesan) in kasus.items():
        meta.write_text(teks, encoding="utf8")
        kode, out = jalankan(skrip, art)
        cek("meta: %s ditolak" % nama, kode == 1 and pesan in out, "exit=%d" % kode)

    meta.write_text(META_BAIK.replace("Kata Kunci Uji | Klien Uji", "Kata Kunci Uji | Termurah"), encoding="utf8")
    kode, out = jalankan(skrip, art)
    cek("meta: klaim 'termurah' hanya WARN", kode == 0 and "superlatif 'termurah'" in out, "exit=%d" % kode)


def uji_parafrase(base):
    """Kedalaman parafrase: hasil humanize yang masih menyalin draft harus ditolak."""
    _, bulan = bikin_skenario(base)
    skrip = ROOT / "alat" / "cek-artikel.py"
    awal = artikel_lulus()
    art = bulan / "uji - Humanized.txt"
    art.write_text(awal, encoding="utf8")
    (bulan / "uji - Meta.txt").write_text(META_BAIK, encoding="utf8")
    kode, out = jalankan(skrip, art)
    cek("parafrase: tanpa draft hanya WARN", kode == 0 and "kedalaman parafrase tidak bisa diukur" in out, "exit=%d" % kode)
    draft = bulan / "uji.txt"
    draft.write_text(awal, encoding="utf8")                      # humanize = salinan draft
    kode, out = jalankan(skrip, art)
    cek("parafrase: salinan draft ditolak (FAIL)", kode == 1 and "parafrase dangkal" in out, "exit=%d" % kode)
    draft.write_text("<p>Teks draft yang sama sekali berbeda dari hasil akhir artikel ini.</p>\n", encoding="utf8")
    kode, out = jalankan(skrip, art)
    cek("parafrase: tulis ulang penuh lolos (hanya INFO)", kode == 0 and "kedalaman parafrase: 0.0%" in out, "exit=%d" % kode)
    kode, out = jalankan(skrip, draft, "--draft")
    cek("parafrase: mode --draft tidak membandingkan draft dengan dirinya", "parafrase" not in out, out[-80:])


def uji_zerogpt(base):
    """siap-zerogpt.py: payload bersih untuk operator, pecah bila panjang, masukan buruk jelas."""
    _, bulan = bikin_skenario(base)
    skrip = ROOT / "alat" / "siap-zerogpt.py"
    art = bulan / "lulus - Humanized.txt"
    art.write_text(artikel_lulus(), encoding="utf8")
    kode, out = jalankan(skrip, art)
    payload = bulan / "payload-zerogpt.txt"
    isi = payload.read_text(encoding="utf8") if payload.is_file() else ""
    bagian = [b for b in isi.split("=====")]
    cek("zerogpt: payload dibuat", kode == 0 and isi != "", out[-60:].replace("\n", " | "))
    cek("zerogpt: payload tanpa tag HTML dan shortcode", "<" not in isi and "whatsapp" not in isi and "Alt text" not in isi)
    cek("zerogpt: tiap bagian maksimal 15000 karakter", all(len(b.strip()) <= 15000 for b in bagian),
        "max=%d" % max((len(b.strip()) for b in bagian), default=0))
    panjang = bulan / "panjang - Humanized.txt"
    panjang.write_text("<p>" + ("Kalimat uji panjang untuk memecah payload menjadi dua bagian. " * 300) + "</p>\n[whatsapp_button id=\"9\"]", encoding="utf8")
    kode, out = jalankan(skrip, panjang)
    isi2 = (bulan / "payload-zerogpt.txt").read_text(encoding="utf8")
    cek("zerogpt: artikel panjang dipecah BAGIAN 1/2", kode == 0 and "BAGIAN 1/2" in isi2 and "=====" in isi2, out[-60:].replace("\n", " | "))
    kode, out = jalankan(skrip, bulan / "tidak-ada.txt")
    cek("zerogpt: berkas tidak ada -> pesan jelas exit 2", kode == 2 and "tidak ada" in out and "Traceback" not in out, "exit=%d" % kode)
    # Payload pendamping tidak boleh terbaca sebagai draft oleh cek-status.
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("zerogpt: cek-status mengabaikan payload-zerogpt", kode == 0 and "payload-zerogpt" not in out, out[:80].replace("\n", " | "))
    # Serah terima: output skrip harus memuat langkah bernomor untuk operator.
    kode, out = jalankan(skrip, art)
    cek("zerogpt: blok TUGAS OPERATOR dengan langkah dan laporan",
        kode == 0 and "TUGAS OPERATOR" in out and "zerogpt.com" in out
        and "Detect Text" in out and "MENUNGGU OPERATOR" in out and "1." in out and "4." in out,
        out[-120:].replace("\n", " | "))


def uji_ai_api(base):
    """cek-ai-api.py: tiruan server lokal (tanpa jaringan nyata dan tanpa kunci asli)."""
    import http.server
    import json
    import threading

    _, bulan = bikin_skenario(base)
    skrip = ROOT / "alat" / "cek-ai-api.py"
    art = bulan / "ai - Humanized.txt"
    art.write_text(artikel_lulus(), encoding="utf8")
    mode = {"kode": 200}

    class Tiruan(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            self.rfile.read(int(self.headers.get("Content-Length", 0)))
            if mode["kode"] != 200:
                self.send_response(mode["kode"])
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error":"x"}')
                return
            badan = {"score": 62.5, "credits_remaining": 123,
                     "attack_detected": {"zero_width_space": False, "homoglyph_attack": False}, "sentences": [
                {"text": "Kalimat terdengar AI sekali di sini.", "score": 12.0},
                {"text": "Kalimat aman dan manusiawi.", "score": 95.0}]}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(badan).encode("utf8"))

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), Tiruan)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    env = dict(os.environ, DCI_AI_API_URL="http://127.0.0.1:%d/" % srv.server_port, WINSTON_API_KEY="kunci-uji")

    def run(*argv, env_pakai=env):
        r = subprocess.run(PY + [str(skrip)] + [str(a) for a in argv], capture_output=True, text=True,
                           timeout=60, env=env_pakai)
        return r.returncode, r.stdout + r.stderr

    kode, out = run(art)
    laporan = bulan / "kalimat-ai.txt"
    isi = laporan.read_text(encoding="utf8") if laporan.is_file() else ""
    cek("ai-api: laporan kalimat ditandai dibuat", kode == 0 and "terdengar AI sekali" in isi
        and "aman dan manusiawi" not in isi and "62.5" in out and "123" in out, out[-80:].replace("\n", " | "))
    cek("ai-api: tanpa peringatan palsu bila semua flag serangan False", "PERINGATAN" not in out, out[:80])
    cek("ai-api: label bukan ZeroGPT dan skor manusia", "BUKAN ZeroGPT" in isi and "MANUSIA" in isi)
    cek("ai-api: kunci tidak tercetak ke keluaran atau laporan", "kunci-uji" not in out and "kunci-uji" not in isi)
    kode, out = run(art, "--ambang", "5")
    cek("ai-api: ambang 5 tidak menandai kalimat", kode == 0 and "Tidak ada kalimat di bawah ambang" in
        laporan.read_text(encoding="utf8"))
    kode, out = run(art, "--ambang", "abc")
    cek("ai-api: ambang tidak sah -> exit 2", kode == 2 and "Traceback" not in out, "exit=%d" % kode)
    env_kosong = {k: v for k, v in env.items() if k != "WINSTON_API_KEY"}
    kode, out = run(art, env_pakai=env_kosong)
    cek("ai-api: tanpa kunci -> pesan jelas exit 2", kode == 2 and "WINSTON_API_KEY" in out and "Traceback" not in out)
    kode, out = run(bulan / "tidak-ada.txt")
    cek("ai-api: berkas tidak ada -> exit 2", kode == 2 and "tidak ada" in out and "Traceback" not in out)
    pendek = bulan / "pendek - Humanized.txt"
    pendek.write_text("Terlalu pendek.", encoding="utf8")
    kode, out = run(pendek)
    cek("ai-api: teks terlalu pendek -> exit 2", kode == 2 and "minimal" in out and "Traceback" not in out)
    mode["kode"] = 401
    kode, out = run(art)
    cek("ai-api: 401 -> pesan kunci salah exit 2", kode == 2 and "Kunci API salah" in out and "Traceback" not in out, out[-60:])
    mode["kode"] = 402
    kode, out = run(art)
    cek("ai-api: 402 -> pesan kredit habis exit 2", kode == 2 and "Kredit Winston habis" in out and "Traceback" not in out)
    env_luar = dict(env, DCI_AI_API_URL="https://contoh-jahat.example/v2/ai-content-detection")
    kode, out = run(art, env_pakai=env_luar)
    cek("ai-api: URL di luar gowinston.ai ditolak sebelum kunci dikirim",
        kode == 2 and "ditolak" in out and "kunci-uji" not in out and "Traceback" not in out, out[-90:])
    srv.shutdown()
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("ai-api: cek-status mengabaikan kalimat-ai.txt", "kalimat-ai" not in out, out[:80].replace("\n", " | "))


def uji_lintas(base):
    skrip = ROOT / "alat" / "cek-artikel.py"
    awal = artikel_lulus()
    # klien A: dua artikel; klien B: satu artikel. CLIENT.md hanya perlu ada untuk klien A.
    klien_a, bulan_a = bikin_skenario(base)
    (bulan_a / "satu - Humanized.txt").write_text(awal, encoding="utf8")
    kode, out = jalankan(skrip, bulan_a / "satu - Humanized.txt")
    cek("lintas: artikel tunggal tidak bentrok dengan dirinya", kode == 0 and "kanibalisasi" not in out and "disalin" not in out, "exit=%d" % kode)

    # keyword sama di klien yang sama -> FAIL kanibalisasi
    kedua = awal.replace("kata-kunci-uji", "kata-kunci-uji-dua")
    (bulan_a / "dua - Humanized.txt").write_text(kedua, encoding="utf8")
    kode, out = jalankan(skrip, bulan_a / "dua - Humanized.txt")
    cek("lintas: keyword sama di klien sama ditolak (kanibalisasi)", kode == 1 and "kanibalisasi" in out, "exit=%d" % kode)

    # kalimat identik di klien lain -> FAIL kalimat disalin, tetapi BUKAN kanibalisasi (beda situs)
    klien_b = base / "Klien Lain"
    bulan_b = klien_b / "artikel" / "2026 April"
    bulan_b.mkdir(parents=True)
    (klien_b / "CLIENT.md").write_text(
        "| `{client_name}` | Klien Lain |\n| `{client_url}` | https://lain.example |\n"
        "| `{client_wa_shortcode}` | `[wa id=\"9\"]` |\n| `{client_phone}` | +62 000 |\n"
        "| `{client_email}` | a@b.example |\n", encoding="utf8")
    salinan = awal.replace("klienuji.example", "lain.example").replace("Klien Uji", "Klien Lain")
    (bulan_b / "tiga - Humanized.txt").write_text(salinan, encoding="utf8")
    kode, out = jalankan(skrip, bulan_b / "tiga - Humanized.txt")
    cek("lintas: kalimat disalin dari klien lain ditolak", kode == 1 and "kalimat disalin" in out, "exit=%d" % kode)
    cek("lintas: keyword sama beda klien BUKAN kanibalisasi", "kanibalisasi" not in out)

    # artikel yang benar-benar berbeda lolos
    beda = awal
    for i, k in enumerate(KALIMAT):
        beda = beda.replace(k, "Kalimat pengganti nomor %d dengan susunan lain sama sekali agar tidak identik." % i)
    beda = beda.replace("Kata Kunci Uji", "Topik Berbeda Sekali").replace("kata-kunci-uji", "topik-berbeda-sekali")
    (bulan_b / "empat - Humanized.txt").write_text(beda, encoding="utf8")
    (bulan_b / "tiga - Humanized.txt").unlink()
    kode, out = jalankan(skrip, bulan_b / "empat - Humanized.txt", "--kw", "Topik Berbeda Sekali")
    cek("lintas: artikel berbeda tidak ditandai salin/kanibalisasi", "disalin" not in out and "kanibalisasi" not in out, "exit=%d" % kode)

    # folder berawalan _ (cetakan) diabaikan
    tmpl = base / "_TEMPLATE" / "artikel" / "YYYY Bulan"
    tmpl.mkdir(parents=True)
    (tmpl / "cetakan - Humanized.txt").write_text(awal, encoding="utf8")
    (bulan_a / "dua - Humanized.txt").unlink()
    kode, out = jalankan(skrip, bulan_a / "satu - Humanized.txt")
    cek("lintas: folder _TEMPLATE diabaikan", "_TEMPLATE" not in out, "exit=%d" % kode)


def uji_template_belum_diisi(base):
    """Klien baru yang menyalin _TEMPLATE tapi belum mengisi CLIENT.md harus dapat pesan jelas."""
    templat = ROOT / "klien" / "_TEMPLATE"
    klien = base / "klien" / "Klien Baru"
    shutil.copytree(templat, klien)
    bulan = klien / "artikel" / "YYYY Bulan"
    (bulan / "draft.txt").write_text("isi\n[whatsapp_button id=\"1\"]\n", encoding="utf8")
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("template: cek-status menolak CLIENT.md bawaan dengan pesan jelas", kode != 0 and "isian bawaan template" in out and "Traceback" not in out, "exit=%d" % kode)
    art = bulan / "a - Humanized.txt"
    art.write_text('<p><a href="https://x.example/artikel/k"><b><i>Kata</i></b></a> - isi.</p>\n', encoding="utf8")
    kode, out = jalankan(ROOT / "alat" / "cek-artikel.py", art, "--kw", "Kata")
    cek("template: cek-artikel menolak CLIENT.md bawaan (exit 2), bukan FAIL menyesatkan", kode == 2 and "isian bawaan template" in out and "tidak muncul di artikel" not in out, "exit=%d" % kode)


def uji_pasang_perintah(base):
    """Pemasang perintah: format per agent benar, placeholder terganti, tidak menyentuh berkas lain."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("pasang_uji", ROOT / "alat" / "pasang-perintah.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)

    sumber = (ROOT / "perintah" / "artikel.md").read_text(encoding="utf8")
    cek("perintah: sumber netral tidak memuat kepala (---) khusus agent", not sumber.lstrip().startswith("---"))
    cek("perintah: sumber memuat penanda yang akan diganti", "{{ARGUMEN}}" in sumber and "{{PYTHON}}" in sumber)
    cek("perintah: sumber tidak merujuk folder agent (.trae/.zcode/.claude)", not re.search(r"\.(trae|zcode|claude)/", sumber))
    cek("perintah: sumber merujuk alat/ yang ada", "alat/cek-artikel.py" in sumber and (ROOT / "alat" / "cek-artikel.py").is_file())

    for nama, info in modul.AGEN.items():
        isi = modul.bangun(info)
        cek("perintah[%s]: tidak ada penanda tersisa" % nama, "{{" not in isi)
        kepala = isi.split("---")[1]
        if info["kepala"] == "trae":
            cek("perintah[trae]: kepala memakai Name dan Description", "Name: artikel" in kepala and "Description:" in kepala)
        else:
            cek("perintah[%s]: kepala memakai description dan argument-hint" % nama,
                "description:" in kepala and "argument-hint:" in kepala)
        cek("perintah[%s]: argumen disisipkan sesuai agent" % nama, info["argumen"] in isi)

    # Pasang ke folder sementara: salinan root palsu supaya repo asli tidak disentuh.
    akar = base / "root"
    (akar / "perintah").mkdir(parents=True)
    (akar / "alat").mkdir()
    shutil.copy(ROOT / "perintah" / "artikel.md", akar / "perintah" / "artikel.md")
    shutil.copy(ROOT / "alat" / "pasang-perintah.py", akar / "alat" / "pasang-perintah.py")
    asing = akar / ".claude" / "commands" / "milik-orang.md"
    asing.parent.mkdir(parents=True)
    asing.write_text("jangan disentuh", encoding="utf8")
    skrip = akar / "alat" / "pasang-perintah.py"
    kode, out = jalankan(skrip, "semua")
    cek("pasang: semua agent terpasang (exit 0)", kode == 0 and out.count("terpasang:") == 3, "exit=%d" % kode)
    cek("pasang: file perintah ada di tiap folder agent",
        all((akar / d / "commands" / "artikel.md").is_file() for d in (".trae", ".zcode", ".claude")))
    cek("pasang: command milik orang lain tidak disentuh", asing.read_text(encoding="utf8") == "jangan disentuh")
    cek("pasang: akhir baris LF", b"\r" not in (akar / ".trae" / "commands" / "artikel.md").read_bytes())
    kode, out = jalankan(skrip, "semua", "--cek")
    cek("pasang: --cek melaporkan sudah terbaru", kode == 0 and out.count("sudah terpasang dan terbaru") == 3, out[:100].replace("\n", " | "))
    (akar / ".zcode" / "commands" / "artikel.md").write_text("usang", encoding="utf8")
    kode, out = jalankan(skrip, "zcode", "--cek")
    cek("pasang: --cek mendeteksi salinan usang tanpa menulis", "berbeda" in out and (akar / ".zcode" / "commands" / "artikel.md").read_text(encoding="utf8") == "usang")
    kode, out = jalankan(skrip, "gemini")
    cek("pasang: agent tidak dikenal ditolak (exit 2)", kode == 2 and "tidak dikenal" in out, "exit=%d" % kode)
    kode, out = jalankan(skrip)
    cek("pasang: tanpa argumen menampilkan daftar (exit 2)", kode == 2 and "Agent yang didukung" in out, "exit=%d" % kode)
    (akar / "perintah" / "artikel.md").unlink()
    kode, out = jalankan(skrip, "trae")
    cek("pasang: sumber hilang -> pesan jelas (exit 2)", kode == 2 and "tidak ada" in out and "Traceback" not in out, "exit=%d" % kode)

    # Skill ikut repo: harus lengkap (SKILL.md dengan name sama nama folder) dan ikut terpasang.
    daftar = sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file())   # pustaka dibaca lewat jalur, tidak dipasang
    cek("skill: ada skill di repo", len(daftar) >= 1)
    for p in daftar:
        kepala = (p / "SKILL.md").read_text(encoding="utf8").split("---")[1]
        cek("skill[%s]: nama di kepala sama dengan nama folder" % p.name, re.search(r"(?m)^name:\s*%s\s*$" % re.escape(p.name), kepala) is not None)
    akar2 = base / "root2"
    (akar2 / "perintah").mkdir(parents=True)
    (akar2 / "alat").mkdir()
    shutil.copy(ROOT / "perintah" / "artikel.md", akar2 / "perintah" / "artikel.md")
    shutil.copy(ROOT / "alat" / "pasang-perintah.py", akar2 / "alat" / "pasang-perintah.py")
    shutil.copytree(ROOT / "skills", akar2 / "skills")
    kode, out = jalankan(akar2 / "alat" / "pasang-perintah.py", "claude")
    cek("skill: terpasang ke .claude/skills", kode == 0 and all((akar2 / ".claude" / "skills" / p.name / "SKILL.md").is_file() for p in daftar), "exit=%d" % kode)
    kode, out = jalankan(akar2 / "alat" / "pasang-perintah.py", "claude", "--cek")
    cek("skill: --cek melaporkan terbaru", kode == 0 and "terbaru" in out and "belum" not in out, out[:100].replace("\n", " | "))


def uji_pustaka():
    """skills/pustaka: lengkap, berlisensi, rujukan INDEKS valid, tanpa skrip/kredensial, terhubung ke AGENT.md."""
    pus = ROOT / "skills" / "pustaka"
    indeks = (pus / "INDEKS.md").read_text(encoding="utf8")
    skill = sorted(p for p in pus.iterdir() if p.is_dir() and p.name != "LISENSI")
    cek("pustaka: ada 13 skill", len(skill) == 13, "jumlah=%d" % len(skill))
    for p in skill:
        sm = p / "SKILL.md"
        kepala = sm.read_text(encoding="utf8").split("---")[1] if sm.is_file() else ""
        cek("pustaka[%s]: SKILL.md ada dan name sama dengan folder" % p.name,
            re.search(r"(?m)^name:\s*%s\s*$" % re.escape(p.name), kepala) is not None)
        cek("pustaka[%s]: disebut di INDEKS" % p.name, "`%s`" % p.name in indeks)
    for lic in ("claude-blog", "marketingskills", "anti-slop"):
        f = pus / "LISENSI" / (lic + ".MIT.txt")
        cek("pustaka: lisensi %s ada (MIT + Copyright)" % lic,
            f.is_file() and "MIT License" in f.read_text(encoding="utf8") and "Copyright" in f.read_text(encoding="utf8"))
    ada = [p for p in pus.rglob("*") if p.is_file()]
    cek("pustaka: tanpa skrip .py (tidak ada yang bisa dijalankan tanpa sengaja)", not [p for p in ada if p.suffix == ".py"])
    cek("pustaka: tanpa folder evals", not [p for p in ada if "evals" in p.parts])
    cek("pustaka: tanpa jalur pribadi atau kunci API",
        not [p for p in ada if p.suffix == ".md" and re.search(r"C:\\Users\\|AIza[0-9A-Za-z_-]{20,}|sk-[A-Za-z0-9]{20,}", p.read_text(encoding="utf8"))])
    # Tiap `blog/references/...` yang disebut INDEKS harus ada di disk.
    putus = [m for m in re.findall(r"`(blog/references/[A-Za-z0-9_.-]+)`", indeks) if not (pus / m).is_file()]
    cek("pustaka: berkas rujukan di INDEKS ada", not putus, ", ".join(putus))
    # Pustaka harus berdiri sendiri: tanpa variabel/subagent/skrip/berbayar yang hanya ada di Claude Code.
    mati = re.compile(r"CLAUDE_SKILL_DIR|CLAUDE_BLOG|CLAUDE_PLUGIN|scripts/|run\.py|blog_preflight|blog_render|"
                      r"analyze_blog|quality_gate|generate_hero|DataForSEO|blog-google|/blog [a-z]|subagent|"
                      r"plan mode|orchestration-details|load_untrusted|BRAND\.md|VOICE\.md|DISCOURSE\.md|"
                      r"\.agents/|\.claude/|product-marketing|tools/REGISTRY|"
                      r"blog-(reviewer|researcher|writer|analyze|audit|chart|image|brand|flow|write|outline|brief|"
                      r"cluster|strategy|calendar|persona|notebooklm|audio|translate|localize|discourse|taxonomy|"
                      r"google|delivery)\b|claude-seo|programmatic-seo|site-architecture|content-strategy|\bcro\b|ab-testing")
    salah = []
    for f in ada:
        if f.suffix == ".md" and f.name != "INDEKS.md":        # INDEKS boleh menyebut nama itu dalam aturan adaptasi
            dalam_komentar = False
            for i, baris in enumerate(f.read_text(encoding="utf8").splitlines(), 1):
                if baris.lstrip().startswith("<!--"):
                    dalam_komentar = True
                if dalam_komentar:                              # catatan adaptasi boleh menyebutnya
                    if "-->" in baris:
                        dalam_komentar = False
                    continue
                if mati.search(baris):
                    salah.append("%s:%d: %s" % (f.relative_to(pus), i, baris.strip()[:70]))
    cek("pustaka: tanpa rujukan Claude Code / skrip / alat berbayar", not salah, " | ".join(salah[:5]))
    agent = (ROOT / "AGENT.md").read_text(encoding="utf8")
    cek("pustaka: AGENT.md menunjuk INDEKS", "skills/pustaka/INDEKS.md" in agent)
    cek("pustaka: skill penunjuk menyebut INDEKS", "skills/pustaka/INDEKS.md" in (ROOT / "skills" / "dci-seo-auditor" / "SKILL.md").read_text(encoding="utf8"))


def uji_inti():
    """aturan/INTI.md: ada, ringkas, dan selaras dengan aturan utama (cliché, ambang, batas putaran)."""
    f = ROOT / "aturan" / "INTI.md"
    cek("inti: berkas ada", f.is_file())
    if not f.is_file():
        return
    teks = f.read_text(encoding="utf8")
    cek("inti: ringkas (maks 80 baris)", len(teks.splitlines()) <= 80, "baris=%d" % len(teks.splitlines()))
    agent = (ROOT / "AGENT.md").read_text(encoding="utf8")
    # Setiap cliché terlarang di Section 11 harus tercantum di INTI.
    blok = re.search(r"FORBIDDEN cliché phrases:(.+)", agent)
    clich = re.findall(r'"([^"]+)"', blok.group(1)) if blok else []
    hilang = [c for c in clich if c not in teks]
    cek("inti: memuat semua cliché terlarang Section 11", bool(clich) and not hilang, "hilang=%s" % hilang)
    cek("inti: ambang keyword dan paragraf pertama sama dengan Section 11",
        "31-34" in teks and "200 kata" in teks and "31-34" in agent and "200 words" in agent)
    cek("inti: batas 2 putaran perbaikan", "Maksimal 2 putaran" in teks)
    cek("inti: ZeroGPT oleh operator", "MENUNGGU OPERATOR" in teks and "TUGAS OPERATOR" in teks)
    cek("inti: ditunjuk AGENTS.md, perintah, dan AGENT.md",
        all("aturan/INTI.md" in (ROOT / p).read_text(encoding="utf8") for p in ("AGENTS.md", "perintah/artikel.md", "AGENT.md")))
    # Semua perintah alat yang disebut INTI harus ada skripnya.
    putus = [m for m in re.findall(r"alat/([a-z-]+\.py)", teks) if not (ROOT / "alat" / m).is_file()]
    cek("inti: skrip yang disebut ada", not putus, ", ".join(putus))


def jalan_menu(root, *masukan):
    """Jalankan menu.py dari salinan root dengan masukan terskrip (tanpa clipboard dan tanpa buka editor)."""
    env = dict(os.environ, DCI_TANPA_SALIN="1", DCI_TANPA_BUKA="1")
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", str(root / "alat" / "menu.py")],
                       input="\n".join(masukan) + "\n", capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=120, env=env, cwd=str(root))
    return r.returncode, r.stdout + r.stderr


def uji_menu(base):
    """Menu interaktif: tiap pilihan menghasilkan bahasa yang mudah dipahami, tanpa traceback."""
    akar = base / "root"
    shutil.copytree(ROOT / "alat", akar / "alat", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "klien" / "_TEMPLATE", akar / "klien" / "_TEMPLATE")
    shutil.copytree(ROOT / "perintah", akar / "perintah")
    shutil.copytree(ROOT / "klien" / "Salimah Catering", akar / "klien" / "Salimah Catering")
    shutil.copy(ROOT / "AGENT.md", akar / "AGENT.md")

    kode, out = jalan_menu(akar, "0")
    cek("menu: tampil dan keluar dengan 0", kode == 0 and "DCI SEO Auditor" in out and "Sampai jumpa" in out and "Traceback" not in out, "exit=%d" % kode)
    kode, out = jalan_menu(akar, "99", "abc", "0")
    cek("menu: pilihan ngawur ditolak dengan sopan", out.count("Pilihan tidak dikenal") >= 2 and "Traceback" not in out)
    kode, out = jalan_menu(akar, "")
    cek("menu: masukan habis (Enter kosong lalu EOF) tidak crash", "Traceback" not in out, "exit=%d" % kode)

    kode, out = jalan_menu(akar, "3", "1", "1", "", "0")
    cek("menu 3: status memakai bahasa biasa, bukan kode mentah", "[SELESAI]" in out and "Tidak perlu dikerjakan lagi" in out and "tahap_kosong" not in out)
    kode, out = jalan_menu(akar, "4", "1", "1", "1", "", "0")
    cek("menu 4: artikel Salimah dinyatakan LULUS", "LULUS" in out and "Traceback" not in out, out[-120:].replace("\n", " | "))
    kode, out = jalan_menu(akar, "2", "1", "1", "", "0")
    cek("menu 2: perintah kerja memuat nama klien, bulan, dan tahun",
        "kerjakan Salimah Catering bulan November 2026" in out, out[-160:].replace("\n", " | "))

    # Artikel dibuat gagal: pesan harus menyebut jumlah masalah dalam bahasa biasa.
    bulan = akar / "klien" / "Salimah Catering" / "artikel" / "2026 November"
    art = bulan / "Jasa Catering Instansi Blitar - Humanized.txt"
    art.write_text(art.read_text(encoding="utf8").replace("<!--more-->", ""), encoding="utf8")
    kode, out = jalan_menu(akar, "4", "1", "1", "1", "", "0")
    cek("menu 4: artikel bermasalah -> BELUM LULUS + daftar bernomor", "BELUM LULUS" in out and "more" in out and "1." in out)

    kode, out = jalan_menu(akar, "5", "Klien Baru Uji", "", "0")
    cek("menu 5: klien baru dibuat dari template", (akar / "klien" / "Klien Baru Uji" / "CLIENT.md").is_file() and "BERHASIL" in out, out[-150:].replace("\n", " | "))
    cek("menu 5: folder bulan memakai tahun dan bulan sekarang (bukan YYYY Bulan)",
        not (akar / "klien" / "Klien Baru Uji" / "artikel" / "YYYY Bulan").exists()
        and len(list((akar / "klien" / "Klien Baru Uji" / "artikel").iterdir())) == 1)
    kode, out = jalan_menu(akar, "5", "Klien Baru Uji", "", "0")
    cek("menu 5: klien yang sudah ada tidak ditimpa", "sudah ada" in out and "Traceback" not in out)
    for buruk in ("a/b", "_rahasia", ".x", 'x*y'):
        kode, out = jalan_menu(akar, "5", buruk, "", "0")
        cek("menu 5: nama '%s' ditolak" % buruk, "tidak boleh" in out and not (akar / "klien" / buruk.replace("/", "")).exists())
    kode, out = jalan_menu(akar, "3", "1", "1", "", "0")
    kode, out = jalan_menu(akar, "1", "4", "", "0")
    cek("menu 1: pasang untuk semua agent berhasil dengan pesan langkah berikut",
        "BERHASIL" in out and "tutup lalu buka lagi" in out, out[-200:].replace("\n", " | "))
    cek("menu 1: berkas /artikel muncul di folder agent",
        all((akar / d / "commands" / "artikel.md").is_file() for d in (".trae", ".zcode", ".claude")))

    kode, out = jalan_menu(akar, "6", "", "0")
    cek("menu 6: bantuan tampil", "Urutan kerja yang biasa" in out and "Traceback" not in out)

    # Tanpa klien sama sekali: pesan jelas.
    shutil.rmtree(akar / "klien" / "Salimah Catering")
    shutil.rmtree(akar / "klien" / "Klien Baru Uji")
    kode, out = jalan_menu(akar, "3", "", "0")
    cek("menu: belum ada klien -> petunjuk ke menu 5", "Belum ada klien" in out and "Traceback" not in out)


def uji_peluncur():
    isi = (ROOT / "MULAI.bat").read_bytes()
    cek("MULAI.bat: akhir baris CRLF (LF merusak goto di cmd)", isi.count(b"\r\n") == isi.count(b"\n") and b"\r\n" in isi)
    teks = isi.decode("utf-8")
    cek("MULAI.bat: UTF-8 diaktifkan dan pindah ke folder berkas", "chcp 65001" in teks and 'cd /d "%~dp0"' in teks)
    cek("MULAI.bat: mencoba py, python, python3 dan punya pesan bila Python tidak ada",
        '"py -3"' in teks and '"python"' in teks and '"python3"' in teks and "Python belum terpasang" in teks)
    cek("MULAI.bat: jendela tidak tertutup sendiri (pause)", "pause" in teks)
    cek("MULAI.bat: hanya ASCII di baris perintah", all(ord(c) < 128 for c in teks))
    if os.name == "nt":
        env = dict(os.environ)
        r = subprocess.run([os.environ.get("ComSpec", "cmd.exe"), "/c", str(ROOT / "MULAI.bat")],
                           input="0\n\n", capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=60, env=env, cwd=os.environ.get("TEMP", "."))
        cek("MULAI.bat: dijalankan dari folder lain, menu muncul dan keluar bersih",
            r.returncode == 0 and "DCI SEO Auditor" in r.stdout and "Sampai jumpa" in r.stdout, "exit=%d" % r.returncode)
        env["PATH"] = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32")
        r = subprocess.run([os.environ.get("ComSpec", "cmd.exe"), "/c", str(ROOT / "MULAI.bat")],
                           input="\n", capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=60, env=env, cwd=os.environ.get("TEMP", "."))
        cek("MULAI.bat: tanpa Python -> petunjuk memasang, bukan error cmd", "Python belum terpasang" in r.stdout and "CENTANG" in r.stdout)
    else:
        print("LEWAT uji MULAI.bat berjalan: hanya untuk Windows")


def uji_masukan_buruk(base):
    """Masukan yang salah harus menghasilkan pesan manusiawi dengan kode 2, bukan traceback."""
    _, bulan = bikin_skenario(base)
    skrip = ROOT / "alat" / "cek-artikel.py"
    kode, out = jalankan(skrip, bulan / "tidak-ada.txt")
    cek("masukan: berkas tidak ada -> pesan jelas, exit 2", kode == 2 and "tidak ada" in out and "Traceback" not in out, "exit=%d" % kode)
    rusak = bulan / "latin1.txt"
    rusak.write_bytes(b"<p>\xe9\xe8</p>")
    kode, out = jalankan(skrip, rusak, "--kw", "x")
    cek("masukan: bukan UTF-8 -> pesan jelas, exit 2", kode == 2 and "UTF-8" in out and "Traceback" not in out, "exit=%d" % kode)
    kosong = bulan / "kosong.txt"
    kosong.write_text("", encoding="utf8")
    kode, out = jalankan(skrip, kosong, "--draft")
    cek("masukan: draft kosong tetap exit 0 (audit bukan penghalang)", kode == 0 and "Traceback" not in out, "exit=%d" % kode)
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("masukan: cek-status tidak crash, draft kosong = MENUNGGU", kode == 0 and "MENUNGGU" in out and "Traceback" not in out, "exit=%d" % kode)
    cek("masukan: cek-status melaporkan berkas bukan UTF-8 sebagai RUSAK, draft lain tetap terbaca",
        re.search(r"RUSAK\t-\ttahap_kosong=-\tlatin1\.txt", out) is not None and "kosong.txt" in out, out[:120].replace("\n", " | "))


def uji_kamus():
    """Kamus offline: kata dasar, imbuhan, dan salah ketik (tanpa jaringan)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("cek_artikel_uji", ROOT / "alat" / "cek-artikel.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    kamus = modul.baca_kamus()
    cek("kamus: memuat puluhan ribu kata dasar", len(kamus) > 40000, "jumlah=%d" % len(kamus))
    for kata in ("makanan", "mengonsumsi", "pengaruhnya", "diutak-atik", "katering", "dipesankan"):
        ok = all(modul.kata_dikenal(b, kamus) for b in kata.split("-"))
        cek("kamus: '%s' dikenali" % kata, ok)
    for kata in ("pelaynan", "kualitsa", "mkanan"):
        cek("kamus: salah ketik '%s' tertangkap" % kata, not modul.kata_dikenal(kata, kamus))
    lisensi = ROOT / "alat" / "kamus-id.LICENSE.txt"
    cek("kamus: berkas lisensi LGPL ikut repo", lisensi.is_file() and "GNU LESSER GENERAL PUBLIC LICENSE" in lisensi.read_text(encoding="utf8").upper())

def main():
    with tempfile.TemporaryDirectory(prefix="uji-dci-seo-") as d:
        base = Path(d)
        uji_status(base)
        uji_artikel(base)
        uji_artikel_lulus(base)
    with tempfile.TemporaryDirectory(prefix="uji-dci-menu-") as d:
        uji_menu(Path(d))
    uji_peluncur()
    with tempfile.TemporaryDirectory(prefix="uji-dci-pasang-") as d:
        uji_pasang_perintah(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-templat-") as d:
        uji_template_belum_diisi(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-masukan-") as d:
        uji_masukan_buruk(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-meta-") as d:
        uji_meta(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-zerogpt-") as d:
        uji_zerogpt(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-aiapi-") as d:
        uji_ai_api(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-lintas-") as d:
        uji_lintas(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-parafrase-") as d:
        uji_parafrase(Path(d))
    uji_kamus()
    uji_pustaka()
    uji_inti()
    print("-" * 60)
    if GAGAL_UJI:
        print("UJI GAGAL: %s" % ", ".join(GAGAL_UJI))
        sys.exit(1)
    print("Semua %d uji lulus." % JUMLAH_UJI[0])


main()
