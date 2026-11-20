---
Name: artikel
Description: DCI SEO Auditor — kerjakan artikel SEO satu klien untuk satu bulan (audit, humanize, cek ZeroGPT, laporan). Format argumen: <nama perusahaan> <bulan> [tahun]
---

Jalankan Mode Pintasan untuk argumen yang user tulis setelah `/artikel`.

Cara membaca argumen:
- Kata terakhir = nama bulan. Bila kata terakhir berupa angka 4 digit, itu tahun dan nama bulan adalah kata sebelumnya.
- Semua kata di depannya = nama perusahaan (boleh lebih dari satu kata).
- Argumen kosong atau tidak bisa dibaca: tanyakan ke operator, jangan menebak.

Skill tidak wajib. Semua aturan ada di repo: baca `aturan/kerja-tanpa-skill.md`. Bila agent memiliki skill pelengkap (antislop-copywriting, blog-rewrite, blog-seo-check, verification-before-completion), boleh dipakai, tetapi jangan mengunduh skill dan jangan berhenti bila tidak ada.

Langkah kerja:
1. Baca `AGENT.md` di ROOT project (folder yang memuat `AGENT.md`) dan `aturan/kerja-tanpa-skill.md`.
2. Ikuti Section 10 (Mode Pintasan) sampai selesai. Pipeline ada di Section 4, checklist di Section 5, ZeroGPT di Section 6, format laporan di Section 7, skill di Section 9, aturan konten lengkap di Section 11.
3. Sebelum audit apa pun, jalankan Gerbang Status (Section 4): `python -I .zcode/cek-status.py "klien/<Klien>/artikel/<YYYY Bulan>"`. Proses hanya draft `BARU` dan `LANJUTKAN`. Draft `SELESAI`, `MENUNGGU`, `BERUBAH`, `TANPA-CATATAN`, dan `RUSAK` tidak boleh disentuh.
4. Audit draft mentah dengan `python -I -X utf8 .zcode/cek-artikel.py "<draft>" --draft`. Daftar TEMUAN-nya menjadi bahan humanize.
5. Setelah humanize, tulis berkas `<artikel> - Meta.txt` (judul SEO, deskripsi meta, slug), lalu jalankan Gerbang Kualitas (Section 4): `python -I -X utf8 .zcode/cek-artikel.py "<artikel>" --kbbi --simpan-kata`. Perbaiki hanya bagian FAIL sampai 0 FAIL. Jangan rombak keseluruhan.
6. Draft asli tidak boleh ditimpa. Ledger dan laporan ditulis ke `LAPORAN.md` folder bulan klien, bukan ke `AGENT.md`. Hash ledger disalin dari output skrip, tidak dihitung manual.
7. Akhiri dengan laporan ringkas di chat: status setiap draft (termasuk yang dilewati), tabel artikel yang diproses, temuan yang butuh keputusan, dan status plagiarisme.

Catatan: contoh perintah memakai `python`. Di macOS atau Linux pakai `python3`.
