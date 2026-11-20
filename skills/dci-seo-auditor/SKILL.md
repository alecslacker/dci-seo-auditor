---
name: dci-seo-auditor
description: Use when the user asks to work on, audit, humanize, or check a WordPress SEO article for a Duta Corpora Indonesia (DCI) client, or says "/artikel", "kerjakan artikel <klien> bulan <bulan>", "cek artikel", "audit artikel". Runs the repo's own pipeline (audit, humanize, quality gate, report) using only files inside the DCI SEO Auditor repo.
---

# DCI SEO Auditor

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved

Skill ini hanya penunjuk. Semua aturan ada di repo DCI SEO Auditor, jadi tidak ada yang perlu dipasang selain skill ini.

## Langkah

1. Pastikan direktori kerja adalah root repo (ada `AGENT.md`, `alat/`, `klien/`). Bila bukan, minta operator membuka repo itu.
2. Baca `AGENT.md` (pipeline, checklist, Section 10 mode `/artikel`, Section 11 aturan konten) dan `aturan/kerja-tanpa-skill.md` (metode menulis ulang, aturan fakta, berkas meta, kanibalisasi).
3. Kerjakan sesuai `AGENT.md` Section 10. Draft asli tidak ditimpa; hasil disimpan sebagai `<nama> - Humanized.txt`.
4. Jangan menyatakan artikel lulus sebelum `python -I -X utf8 alat/cek-artikel.py "<artikel>"` dijalankan pada berkas terbaru dan menunjukkan `0 FAIL` (di macOS/Linux pakai `python3`).

## Larangan

- Jangan mengarang statistik, testimoni, nama, harga, atau fakta kota.
- Data satu klien tidak boleh muncul di artikel klien lain.
- Jangan mengunduh skill lain. Skill tidak wajib untuk pipeline ini.
