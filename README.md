# Content Ops AI Puffer — Artikel SEO Multi-Klien via ZCode

> Pipeline otomatis untuk mengubah draft artikel mentah hasil AI menjadi artikel WordPress yang lolos
> Rank Math (80–100), lolos detektor AI, berbahasa Indonesia baku, dan tercatat rapi per klien.
> Dibangun dan dijalankan dengan [ZCode](https://zcode.ai) — satu perintah, banyak perusahaan.

```text
draft mentah (AI Puffer) ──► AUDIT ──► HUMANIZE ──► GERBANG KUALITAS ──► ZeroGPT ──► LAPORAN
                              ^                                    │
                              └──── perbaiki hanya bagian FAIL ─────┘
```

## Fitur

- **Satu perintah untuk semua klien** — `/artikel <nama perusahaan> <bulan>` (command ZCode di `.zcode/commands/artikel.md`).
- **Gerbang status** — draft yang sudah diaudit tidak pernah diaudit dua kali; penulis yang bekerja bertahap aman (status: `BARU`, `MENUNGGU`, `LANJUTKAN`, `SELESAI`, `BERUBAH`, `TANPA-CATATAN`).
- **Audit otomatis draft mentah** — daftar temuan bernomor: komponen wajib, ejaan tidak baku, kata asing, angka tanpa label, dan pola khas AI (ritme seragam, rule-of-three, marker percakapan berlebih).
- **Gerbang kualitas final** — Rank Math (kata, paragraf pertama, keyword 31–34× bold, density 1–1,5%, heading), format WordPress (`<!--more-->`, `<p>&nbsp;</p>`, list, alt text, shortcode), dan Anti-Typo Gate; lulus = `0 FAIL`.
- **Verifikasi bahasa ke KBBI Daring** — kata asing ditulis ulang ke padanan baku (nasi box → nasi kotak, snack box → kotak kudapan, dessert → pencuci mulut, dst); kamus tersimpan dan dipakai ulang antar klien.
- **Satu sumber fakta SEO** — `FAKTA-SEO.md` berisi kutipan Google Search Central & Rank Math beserta tanggal resminya, bukan ingatan model.
- **Laporan per klien per bulan** — ledger sidik jari + blok laporan di `LAPORAN.md`; `AGENT.md` tetap netral tanpa data klien.

## Struktur

```text
.
├── AGENT.md                 # otak project: pipeline, checklist, protokol, mode pintasan
├── FAKTA-SEO.md             # fakta Google/Rank Math bersumber + tanggal
├── PROMPT PINTASAN.md       # panduan /artikel + prompt cadangan
├── CHANGELOG.txt            # riwayat perubahan sistem
├── CLAUDE.md                # satu baris: @AGENT.md (impor untuk Claude Code)
├── .zcode/
│   ├── commands/artikel.md  # command /artikel
│   ├── cek-status.py        # gerbang status draft (anti audit dobel)
│   ├── cek-artikel.py       # audit (--draft) & gerbang kualitas final
│   ├── kamus-kata.txt       # kamus kata sah hasil verifikasi KBBI
│   └── uji-tools.py         # uji otomatis 13 skenario kedua gerbang
└── <Nama Klien>/
    ├── CLIENT.md            # data klien (template di AGENT.md Section 3)
    └── artikel/<YYYY Bulan>/
        ├── <slug>.txt               # draft mentah (arsip, tidak ditimpa)
        ├── <slug> - Humanized.txt   # hasil final siap paste ke WordPress
        └── LAPORAN.md               # ledger + laporan audit & crosscheck
```

## Memulai

Prasyarat: ZCode (atau agent lain yang membaca `AGENT.md`) + Python 3.8+ di PATH.

1. **Daftarkan klien**: buat folder `<Nama Klien>/`, salin template `CLIENT.md` dari `AGENT.md` Section 3, isi data (URL, kontak, shortcode WA, istilah brand yang dipertahankan).
2. **Taruh draft**: `<Nama Klien>/artikel/<YYYY Bulan>/<judul>.txt` (hasil mentah plugin AI Puffer).
3. **Jalankan** di ZCode dengan ROOT project sebagai workspace:

   ```text
   /artikel Salimah Catering November
   ```

   Tanpa command, pakai prompt cadangan: `@AGENT.md Kerjakan Salimah Catering bulan November.`

4. **Ambil hasil**: `<judul> - Humanized.txt` siap ditempel ke editor WordPress; `LAPORAN.md` memuat metrik, skor ZeroGPT, dan catatan risiko.

## Alat bawaan

| Perintah | Fungsi |
|---|---|
| `python3 -I -X utf8 .zcode/cek-status.py "<klien>/artikel/<bulan>"` | Klasifikasi draft sebelum dikerjakan |
| `python3 -I -X utf8 .zcode/cek-artikel.py "<draft>" --draft` | Audit draft mentah → daftar temuan |
| `python3 -I -X utf8 .zcode/cek-artikel.py "<artikel>"` | Gerbang kualitas final (exit 1 bila ada FAIL) |
| `python3 -I -X utf8 .zcode/cek-artikel.py "<artikel>" --kbbi --simpan-kata` | Verifikasi kata ke KBBI Daring + simpan kamus |
| `python3 -I -X utf8 .zcode/uji-tools.py` | Uji otomatis kedua gerbang (jalankan setelah mengubah skrip) |

Catatan kuota: pencarian KBBI Daring tanpa akun dibatasi harian — jika lookup massal terhenti, lanjutkan di hari berikutnya; kamus tersimpan sehingga tidak mengulang dari nol.

## Crosscheck ZeroGPT

Versi final dipindai di <https://www.zerogpt.com/> (target: verdict *Human written*, AI < 10%).
Batas gratis 15.000 karakter — payload prosa otomatis dibersihkan dari blok editor sebelum ditempel.
Hasil direkam ke `LAPORAN.md` klien.

## Status

Contoh terverifikasi: artikel *Jasa Catering Instansi Blitar* (Salimah Catering) — 2.073 kata,
keyword 31× (density 1,50%), gerbang `0 FAIL 0 WARN`, ZeroGPT **AI 3,7% (Human written)**.
Rincian di `Salimah Catering/artikel/2026 November/LAPORAN.md`.

---

Author: Mas Wondho — Duta Corpora Indonesia (DCI)
Copyright © 2026 Duta Corpora Indonesia — All rights reserved
