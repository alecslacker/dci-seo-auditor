# DCI SEO Auditor: Agentic SEO Auditor by Duta Corpora Indonesia

DCI SEO Auditor mengubah draft artikel mentah dari plugin AI Puffer menjadi artikel WordPress yang siap tayang. Agent mengerjakan audit, penulisan ulang, dan pemeriksaan. Tiga skrip Python menjadi gerbang yang memutuskan lulus atau tidaknya, jadi hasilnya tidak bergantung pada penilaian agent sendiri.

Tool ini dibuat untuk karyawan Duta Corpora Indonesia. Cara agent menyapa operator mengikuti `AGENTS.md` atau persona di komputer masing-masing.

Target tiap artikel: skor Rank Math 80 sampai 100, bahasa Indonesia baku, lolos ZeroGPT, dan tercatat per klien.

```text
draft mentah ──► GERBANG STATUS ──► AUDIT ──► HUMANIZE ──► GERBANG KUALITAS ──► ZeroGPT ──► LAPORAN
                                                                  │
                                       perbaiki hanya bagian FAIL ◄┘
```

## Cara kerja

1. **Gerbang status.** `cek-status.py` membandingkan sidik jari isi draft dengan ledger di `LAPORAN.md`. Draft yang sudah diaudit tidak diaudit dua kali, dan draft yang masih ditulis penulis dilewati.
2. **Audit.** `cek-artikel.py --draft` mengeluarkan daftar temuan bernomor: komponen wajib, ejaan tidak baku, kata asing, angka tanpa label, dan pola khas tulisan AI.
3. **Humanize.** Agent menulis ulang berdasarkan daftar temuan. Statistik, testimoni, dan nama tidak boleh dikarang.
4. **Gerbang kualitas.** `cek-artikel.py` memeriksa kata, paragraf pertama, keyword, heading, format WordPress, dan ejaan. Artikel lulus bila hasilnya `0 FAIL`.
5. **ZeroGPT dan laporan.** Hasil dipindai di ZeroGPT, lalu angkanya dicatat apa adanya di `LAPORAN.md` klien.

Enam status draft: `BARU`, `MENUNGGU`, `LANJUTKAN`, `SELESAI`, `BERUBAH`, `TANPA-CATATAN`. Artinya ada di `AGENT.md` Section 4.

## Struktur

```text
.
├── AGENTS.md                # penunjuk pendek (±500 token) yang dimuat agent otomatis
├── AGENT.md                 # aturan kerja: pipeline, checklist, protokol, template prompt
├── FAKTA-SEO.md             # fakta Google dan Rank Math, lengkap sumber dan tanggal
├── aturan/
│   └── kerja-tanpa-skill.md # aturan kerja mandiri, tanpa skill apa pun
├── PROMPT PINTASAN.md       # panduan /artikel dan prompt cadangan
├── CHANGELOG.txt            # riwayat perubahan sistem
├── CLAUDE.md                # impor AGENTS.md untuk Claude Code
├── .trae/
│   └── commands/artikel.md  # command /artikel untuk TRAE
├── .zcode/
│   ├── cek-status.py        # gerbang status draft
│   ├── cek-artikel.py       # audit draft dan gerbang kualitas final
│   ├── kamus-kata.txt       # kamus kata hasil verifikasi KBBI
│   └── uji-tools.py         # uji otomatis kedua gerbang
└── klien/                   # semua data klien ada di sini
    ├── _TEMPLATE/           # cetakan klien baru
    └── <Nama Klien>/
        ├── CLIENT.md        # data klien
        └── artikel/<YYYY Bulan>/
            ├── <slug>.txt              # draft mentah (arsip, tidak ditimpa)
            ├── <slug> - Humanized.txt  # hasil akhir, siap tempel ke WordPress
            ├── <slug> - Meta.txt       # judul SEO, deskripsi meta, slug
            └── LAPORAN.md              # ledger dan laporan bulan itu
```

Folder berawalan `_` bukan klien dan tidak pernah diproses.

## Memulai

Butuh agent apa pun yang bisa membaca berkas biasa (TRAE, ZCode, Claude Code, Codex, dan lainnya) dan Python 3.8 ke atas. Tidak perlu memasang skill: semua aturan ada di repo ini (`aturan/kerja-tanpa-skill.md`). Di Windows, jalankan skrip dengan `python`. Contoh di dokumen memakai `python3`.

1. **Daftarkan klien.** Salin `klien/_TEMPLATE/` menjadi `klien/<Nama Klien>/`, ganti nama folder `YYYY Bulan` menjadi bulan kerja, lalu isi semua field di `CLIENT.md`.
2. **Taruh draft.** Simpan draft mentah dari AI Puffer di `klien/<Nama Klien>/artikel/<YYYY Bulan>/<judul>.txt`.
3. **Jalankan** di TRAE dengan root project sebagai workspace:

   ```text
   /artikel Salimah Catering November
   ```

   Tanpa command, pakai prompt cadangan: `@AGENT.md Kerjakan Salimah Catering bulan November.`
4. **Ambil hasil.** `<judul> - Humanized.txt` siap ditempel ke editor WordPress. `LAPORAN.md` memuat metrik, angka ZeroGPT, dan catatan risiko.

## Alat bawaan

| Perintah | Fungsi |
|---|---|
| `python3 -I .zcode/cek-status.py "klien/<klien>/artikel/<bulan>"` | Klasifikasi draft sebelum dikerjakan |
| `python3 -I -X utf8 .zcode/cek-artikel.py "<draft>" --draft` | Audit draft mentah, keluar daftar temuan |
| `python3 -I -X utf8 .zcode/cek-artikel.py "<artikel>"` | Gerbang kualitas final, exit 1 bila ada FAIL |
| `python3 -I -X utf8 .zcode/cek-artikel.py "<artikel>" --kbbi --simpan-kata` | Cek kata ke KBBI Daring dan simpan ke kamus |
| `python3 -I -X utf8 .zcode/uji-tools.py` | Uji otomatis kedua gerbang. Jalankan setelah mengubah skrip |

Pencarian KBBI Daring tanpa akun dibatasi harian. Bila pencarian massal terhenti, lanjutkan keesokan harinya. Kamus tersimpan, jadi kata yang sudah lolos tidak dicek ulang.

## ZeroGPT

Versi final dipindai di <https://www.zerogpt.com/>. Targetnya verdict *Human written* dengan AI di bawah 10%. Batas gratis 15.000 karakter, jadi blok editor dibuang dulu sebelum teks ditempel. Bila lebih panjang, teks dipecah di batas paragraf dan kedua angkanya dilaporkan. Plagiarisme belum punya alat cek otomatis.

## Contoh terverifikasi

Artikel *Jasa Catering Instansi Blitar* milik Salimah Catering: 2.073 kata, keyword 31 kali (density 1,50%), gerbang `0 FAIL 0 WARN`, ZeroGPT AI 3,7% (*Human written*). Rinciannya ada di `klien/Salimah Catering/artikel/2026 November/LAPORAN.md`.

---

Author: Mas Wondho — Duta Corpora Indonesia (DCI)
Copyright © 2026 Duta Corpora Indonesia — All rights reserved
