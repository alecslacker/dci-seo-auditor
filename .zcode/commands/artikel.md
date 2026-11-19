---
description: Kerjakan artikel AI Puffer satu klien untuk satu bulan (audit, humanize, cek ZeroGPT, laporan)
argument-hint: <nama perusahaan> <bulan> [tahun]
skills: antislop-copywriting, blog-rewrite, blog-seo-check, verification-before-completion
---
Jalankan Mode Pintasan untuk argumen berikut: $ARGUMENTS

Cara membaca argumen:
- Kata terakhir = nama bulan. Bila kata terakhir berupa angka 4 digit, itu tahun dan nama bulan adalah kata sebelumnya.
- Semua kata di depannya = nama perusahaan (boleh lebih dari satu kata).
- Argumen kosong atau tidak bisa dibaca: tanyakan ke operator, jangan menebak.

Langkah kerja:
1. Baca `AGENT.md` di ROOT project (folder yang memuat `AGENT.md`).
2. Ikuti Section 10 (Mode Pintasan) sampai selesai. Pipeline ada di Section 4, checklist di Section 5, ZeroGPT di Section 6, format laporan di Section 7, skill di Section 9, aturan konten lengkap di Section 11.
3. Sebelum audit apa pun, jalankan Gerbang Status (Section 4): `python3 -I .zcode/cek-status.py "<Klien>/artikel/<YYYY Bulan>"`. Proses hanya draft `BARU` dan `LANJUTKAN`. Draft `SELESAI`, `MENUNGGU`, `BERUBAH`, dan `TANPA-CATATAN` tidak boleh disentuh.
4. Audit draft mentah dengan `python3 -I -X utf8 .zcode/cek-artikel.py "<draft>" --draft` — daftar TEMUAN-nya menjadi bahan humanize.
5. Setelah humanize, jalankan Gerbang Kualitas (Section 4): `python3 -I -X utf8 .zcode/cek-artikel.py "<artikel>" --kbbi --simpan-kata`. Perbaiki hanya bagian FAIL sampai 0 FAIL; jangan rombak keseluruhan.
5. Draft asli tidak boleh ditimpa. Ledger dan laporan ditulis ke `LAPORAN.md` folder bulan klien, bukan ke `AGENT.md`. Hash ledger disalin dari output skrip, tidak dihitung manual.
6. Akhiri dengan laporan ringkas di chat: status setiap draft (termasuk yang dilewati), tabel artikel yang diproses, temuan yang butuh keputusan, dan status plagiarisme.
