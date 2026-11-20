#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Menu DCI SEO Auditor: semua pekerjaan lewat pilihan angka, tanpa mengetik perintah.

Cara pakai di Windows: klik dua kali MULAI.bat di folder utama project.
Cara lain: python -X utf8 alat/menu.py

Author: Mas Wondho - Duta Corpora Indonesia (DCI)
Copyright (c) 2026 Duta Corpora Indonesia - All rights reserved
"""
import datetime
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALAT = ROOT / "alat"
KLIEN = ROOT / "klien"
AGEN = ["trae", "zcode", "claude"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
STATUS = {
    "BARU": "baru, belum pernah dikerjakan. Siap diproses.",
    "MENUNGGU": "belum lengkap (penulis masih bekerja). Dilewati.",
    "LANJUTKAN": "sudah dikerjakan sebagian. Hanya tahap yang kosong dilanjutkan.",
    "SELESAI": "sudah selesai semua tahap. Tidak perlu dikerjakan lagi.",
    "BERUBAH": "diedit setelah dikerjakan. Tanyakan dulu apakah mau dikerjakan ulang.",
    "TANPA-CATATAN": "hasil akhir ada, tetapi belum tercatat di laporan. Jangan disentuh dulu.",
    "RUSAK": "berkas bukan UTF-8. Simpan ulang sebagai UTF-8 di editor teks.",
}


def garis(ch="-"):
    print(ch * 60)


def judul(teks):
    print()
    garis("=")
    print("  " + teks)
    garis("=")


def tanya(teks):
    try:
        return input(teks).strip()
    except EOFError:
        return "0"


def jeda():
    try:
        input("\nTekan Enter untuk kembali ke menu...")
    except EOFError:
        pass


def pilih(daftar, petunjuk):
    """Tampilkan daftar bernomor. Kembalikan item terpilih, atau None bila batal (0)."""
    if not daftar:
        return None
    for i, d in enumerate(daftar, 1):
        print("  %d. %s" % (i, d))
    print("  0. Kembali")
    while True:
        j = tanya("\n%s [angka]: " % petunjuk)
        if j in ("0", ""):
            return None
        if j.isdigit() and 1 <= int(j) <= len(daftar):
            return daftar[int(j) - 1]
        print("  Pilihan tidak dikenal. Ketik angka yang ada di daftar.")


def jalankan(skrip, *arg):
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", str(ALAT / skrip)] + list(arg),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT))
    return r.returncode, (r.stdout + r.stderr)


def daftar_klien():
    if not KLIEN.is_dir():
        return []
    return sorted(d.name for d in KLIEN.iterdir()
                  if d.is_dir() and not d.name.startswith("_") and (d / "CLIENT.md").is_file())


def daftar_bulan(klien):
    akar = KLIEN / klien / "artikel"
    if not akar.is_dir():
        return []
    return sorted((d.name for d in akar.iterdir() if d.is_dir()), reverse=True)


def pilih_klien_bulan():
    k = daftar_klien()
    if not k:
        print("\nBelum ada klien. Pilih menu 5 (Tambah klien baru) dulu.")
        return None, None
    print("\nPilih klien:")
    klien = pilih(k, "Nomor klien")
    if not klien:
        return None, None
    b = daftar_bulan(klien)
    if not b:
        print("\nKlien ini belum punya folder bulan di klien/%s/artikel/." % klien)
        return None, None
    print("\nPilih bulan kerja:")
    bulan = pilih(b, "Nomor bulan")
    return (klien, bulan) if bulan else (None, None)


def salin_ke_clipboard(teks):
    if os.environ.get("DCI_TANPA_SALIN") == "1" or os.name != "nt":
        return False
    perintah = ["powershell", "-NoProfile", "-NonInteractive", "-Command",
                "[Console]::InputEncoding=[Text.UTF8Encoding]::new(); Set-Clipboard -Value ([Console]::In.ReadToEnd())"]
    try:
        return subprocess.run(perintah, input=teks, text=True, encoding="utf-8",
                              capture_output=True, timeout=20).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


# ---------------------------------------------------------------- aksi menu

def aksi_pasang():
    judul("1. Siapkan komputer: pasang perintah /artikel")
    print("Langkah ini cukup sekali. Pilih program AI yang Anda pakai.")
    print("(Tanda * berarti program itu terdeteksi di komputer ini.)\n")
    nama = ["%s%s" % (a.upper(), " *" if (Path.home() / ("." + a)).is_dir() else "") for a in AGEN]
    nama.append("Semua yang didukung")
    p = pilih(nama, "Program AI Anda")
    if not p:
        return
    target = AGEN if p.startswith("Semua") else [AGEN[nama.index(p)]]
    kode, out = jalankan("pasang-perintah.py", *target)
    if kode == 0:
        print("\nBERHASIL. Perintah /artikel sudah dipasang untuk: %s." % ", ".join(t.upper() for t in target))
        print("Langkah berikut: tutup lalu buka lagi program AI Anda, ketik /artikel di kotak chat.")
        print("Bila tetap tidak muncul, pakai menu 2 (Salin perintah kerja) lalu tempel ke chat.")
    else:
        print("\nGAGAL memasang. Pesan dari sistem:\n" + out.strip()[-400:])


def aksi_salin():
    judul("2. Salin perintah kerja untuk ditempel ke program AI")
    klien, bulan = pilih_klien_bulan()
    if not klien:
        return
    nama_bulan = bulan.split(" ", 1)[1] if " " in bulan else bulan
    tahun = bulan.split(" ", 1)[0] if bulan[:4].isdigit() else ""
    prompt = "Baca AGENT.md, lalu kerjakan %s bulan %s%s sesuai Section 10 (Mode Pintasan)." % (
        klien, nama_bulan, (" " + tahun) if tahun else "")
    print("\nPerintah yang disiapkan:\n")
    print("  " + prompt)
    if salin_ke_clipboard(prompt):
        print("\nSUDAH DISALIN. Buka program AI Anda (dengan folder project ini), lalu tekan Ctrl+V dan Enter.")
    else:
        print("\nTidak bisa menyalin otomatis. Blok tulisan di atas, salin, lalu tempel ke program AI Anda.")


def aksi_status():
    judul("3. Lihat status draft")
    klien, bulan = pilih_klien_bulan()
    if not klien:
        return
    kode, out = jalankan("cek-status.py", "klien/%s/artikel/%s" % (klien, bulan))
    baris = [b for b in out.splitlines() if b.strip()]
    ada = False
    print()
    for b in baris:
        bagian = b.split("\t")
        if len(bagian) >= 4 and bagian[0] in STATUS:
            ada = True
            print("  [%s] %s\n      -> %s" % (bagian[0], bagian[3], STATUS[bagian[0]]))
    if not ada:
        pesan = [b for b in baris if b.startswith("GAGAL")]
        print("  " + (pesan[0] if pesan else "Tidak ada draft (.txt) di folder bulan ini."))


def aksi_periksa():
    judul("4. Periksa artikel hasil akhir")
    klien, bulan = pilih_klien_bulan()
    if not klien:
        return
    folder = KLIEN / klien / "artikel" / bulan
    berkas = sorted(f.name for f in folder.glob("* - Humanized.txt"))
    if not berkas:
        print("\nBelum ada artikel hasil akhir (berkas '... - Humanized.txt') di folder ini.")
        return
    print("\nPilih artikel:")
    nama = pilih(berkas, "Nomor artikel")
    if not nama:
        return
    kode, out = jalankan("cek-artikel.py", "klien/%s/artikel/%s/%s" % (klien, bulan, nama))
    print()
    if kode == 0:
        print("  LULUS. Tidak ada masalah yang harus diperbaiki.")
    elif kode == 1:
        gagal = [b[5:].strip() for b in out.splitlines() if b.startswith("FAIL:")]
        print("  BELUM LULUS. Ada %d hal yang harus diperbaiki:\n" % len(gagal))
        for i, g in enumerate(gagal[:15], 1):
            print("  %2d. %s" % (i, g))
        if len(gagal) > 15:
            print("  ... dan %d lagi." % (len(gagal) - 15))
    else:
        pesan = [b for b in out.splitlines() if b.startswith("GAGAL")]
        print("  TIDAK BISA DIPERIKSA.\n  " + (pesan[0] if pesan else out.strip()[-300:]))
    peringatan = [b[5:].strip() for b in out.splitlines() if b.startswith("WARN:")]
    if peringatan:
        print("\n  Catatan (tidak menghalangi lulus):")
        for p in peringatan[:5]:
            print("   - " + p[:110])


def aksi_klien_baru():
    judul("5. Tambah klien baru")
    nama = tanya("Nama klien/perusahaan (kosongkan untuk batal): ")
    if not nama:
        return
    if re.search(r'[\\/:*?"<>|]', nama) or nama.startswith(("_", ".")):
        print("\nNama tidak boleh memuat \\ / : * ? \" < > | dan tidak boleh diawali _ atau titik.")
        return
    tujuan = KLIEN / nama
    if tujuan.exists():
        print("\nKlien '%s' sudah ada. Tidak ada yang diubah." % nama)
        return
    shutil.copytree(KLIEN / "_TEMPLATE", tujuan)
    hari = datetime.date.today()
    nama_bulan = "%d %s" % (hari.year, BULAN[hari.month - 1])
    (tujuan / "artikel" / "YYYY Bulan").rename(tujuan / "artikel" / nama_bulan)
    print("\nBERHASIL. Folder klien dibuat: klien/%s/" % nama)
    print("Folder bulan kerja: artikel/%s/" % nama_bulan)
    print("\nYang harus Anda lakukan sekarang:")
    print("  1. Isi SEMUA data di CLIENT.md (nama, alamat web, nomor WA, email, kode tombol WA).")
    print("  2. Simpan draft artikel (.txt) dari AI Puffer ke folder bulan di atas.")
    if os.name == "nt" and os.environ.get("DCI_TANPA_BUKA") != "1":
        try:
            os.startfile(str(tujuan / "CLIENT.md"))
            print("\n(CLIENT.md dibuka otomatis di editor.)")
        except OSError:
            pass


def aksi_bantuan():
    judul("6. Bantuan singkat")
    print("""Urutan kerja yang biasa:
  1. Menu 5  : tambah klien baru (hanya sekali per klien).
  2. Simpan draft dari AI Puffer ke folder klien (menu 5 menunjukkan lokasinya).
  3. Menu 2  : salin perintah kerja, lalu tempel ke program AI Anda.
  4. Program AI mengerjakan artikelnya sampai selesai.
  5. Menu 4  : periksa hasilnya. Targetnya LULUS.
  6. Hasil akhir: berkas '... - Humanized.txt' di folder bulan klien.

Hal yang perlu diingat:
  - Draft asli tidak pernah ditimpa.
  - Menu 3 aman dipakai kapan saja, hanya membaca.
  - Panduan lengkap: berkas README.md dan PROMPT PINTASAN.md.""")


AKSI = [("Siapkan komputer (pasang perintah /artikel, cukup sekali)", aksi_pasang),
        ("Salin perintah kerja untuk ditempel ke program AI", aksi_salin),
        ("Lihat status draft sebuah klien", aksi_status),
        ("Periksa artikel hasil akhir", aksi_periksa),
        ("Tambah klien baru", aksi_klien_baru),
        ("Bantuan", aksi_bantuan)]


def main():
    while True:
        judul("DCI SEO Auditor - Duta Corpora Indonesia")
        for i, (nama, _) in enumerate(AKSI, 1):
            print("  %d. %s" % (i, nama))
        print("  0. Keluar")
        j = tanya("\nPilih pekerjaan [angka]: ")
        if j == "0":
            print("\nSampai jumpa.")
            return 0
        if j.isdigit() and 1 <= int(j) <= len(AKSI):
            try:
                AKSI[int(j) - 1][1]()
            except KeyboardInterrupt:
                print("\n(Dibatalkan.)")
            except Exception as e:  # pesan manusiawi, bukan traceback
                print("\nTerjadi masalah tak terduga: %s\nCatat pesan ini dan laporkan ke admin." % e)
            jeda()
        else:
            print("\nPilihan tidak dikenal. Ketik angka 0 sampai %d." % len(AKSI))


if __name__ == "__main__":
    sys.exit(main())
