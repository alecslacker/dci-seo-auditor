# AGENTS.md — DCI SEO Auditor

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved

Project ini mengerjakan artikel SEO WordPress untuk klien Duta Corpora Indonesia. Berkas ini sengaja pendek. Aturan lengkap ada di berkas lain, dan dibaca hanya saat tugasnya artikel.

## Kapan membaca aturan lengkap

Bila tugasnya mengerjakan, mengaudit, atau memeriksa artikel klien (`klien/<Nama Klien>/artikel/...`), baca dua berkas ini sebelum mulai:

1. `AGENT.md`: pipeline, checklist, aturan konten (Section 11), dan mode pintasan `/artikel` (Section 10).
2. `aturan/kerja-tanpa-skill.md`: metode menulis ulang, aturan fakta, disiplin bukti, berkas meta, dan aturan kanibalisasi.

Untuk tugas lain di repo ini (misalnya mengubah skrip di `.zcode/`), berkas di atas tidak perlu dibaca.

## Hal yang tidak boleh ditawar

- Skill tidak wajib. Jangan mengunduh skill, dan jangan berhenti bila skill tidak ada.
- Jangan menyatakan artikel lulus sebelum `python -I -X utf8 .zcode/cek-artikel.py "<artikel>"` dijalankan pada berkas terbaru dan menunjukkan `0 FAIL`. Di macOS atau Linux pakai `python3`.
- Jangan mengarang statistik, testimoni, nama, harga, atau fakta kota. Tidak ada sumber, tidak ditulis.
- Draft asli tidak ditimpa. Hasil akhir disimpan sebagai `<nama> - Humanized.txt`.
- Data satu klien tidak boleh muncul di artikel klien lain.

## Menyapa operator

Cara menyapa mengikuti `AGENTS.md` atau persona yang ada di komputer masing-masing karyawan. Berkas ini tidak menetapkan nama sapaan.

## Menjalankan

Di TRAE, ketik `/artikel <nama perusahaan> <bulan> [tahun]`. Di agent lain, tulis: `Baca AGENT.md, lalu kerjakan <nama perusahaan> bulan <bulan> sesuai Section 10.`
