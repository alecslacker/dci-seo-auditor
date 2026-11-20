# Pustaka Skill SEO dan Audit (DCI SEO Auditor)

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved
> Isi folder ini berasal dari proyek MIT pihak ketiga (rincian di bagian Sumber). Teks lisensinya ada di `LISENSI/`.

Folder ini membawa skill SEO dan audit ke dalam repo, supaya karyawan yang tidak memasang skill apa pun tetap bisa memakainya. **Tidak ada yang perlu dipasang.** Skill dipanggil dengan cara membaca berkasnya: `skills/pustaka/<nama>/SKILL.md`. Cara ini sama untuk TRAE, ZCode, Claude Code, Codex, dan agent lain.

Bila agent punya fitur skill sendiri, abaikan fitur itu untuk folder ini. Baca berkas lewat jalurnya.

## Aturan adaptasi (WAJIB, mengalahkan isi skill)

Skill di sini ditulis untuk blog umum dan alat lain. Di repo ini, aturan berikut menang:

1. **Urutan menang:** `AGENT.md` Section 11 → `aturan/kerja-tanpa-skill.md` → skill di folder ini. Gerbang kelulusan tetap `alat/cek-artikel.py` dengan `0 FAIL`. Skor 100 poin atau checklist di skill hanya bahan pertimbangan, bukan gerbang.
2. **Tidak ada plan mode dan tidak ada menunggu persetujuan.** Mode `/artikel` adalah eksekusi penuh. Abaikan kalimat "enter plan mode", "wait for user approval", dan sejenisnya di `blog-rewrite`.
3. **antislop: tanpa wizard dan tanpa pertanyaan mode.** Lewati "First-Run Install Wizard", "Two Usage Modes", dan pengumuman `antislop active`. Anggap mode `during`. Jangan menulis ke `AGENTS.md`, `CLAUDE.md`, atau berkas pengaturan. Jangan mengunduh apa pun.
4. **antislop hanya untuk tulisan.** Pakai `antislop-copywriting` dan, dari `antislop/SKILL.md`, hanya bagian "Copywriting & Content" serta aturan R-02, R-15, R-16, R-17, R-18, R-36, R-38. Bagian UI, warna, layout, dan dial desain dilewati. Jangan membaca `antislop/SKILL.md` penuh (±60 KB).
5. **Dilarang menjalankan alat berbayar atau berkredensial:** `blog-google`, DataForSEO (mode API `blog-cannibalization`), dan skrip `.py` milik skill blog. Skrip itu memang tidak disertakan. Kanibalisasi di repo ini sudah diperiksa `alat/cek-artikel.py`.
6. **Rujukan yang tidak ada di folder ini dilewati, bukan dicari:** `blog-google`, `blog-brand`, `blog-chart`, `scripts/`, `templates/`, `data/`, dan `agents/`. Itu bagian dari paket aslinya yang tidak disertakan.
7. **Bagian yang tidak berlaku untuk artikel klien DCI:** pembuatan gambar dan chart, video embed, `dateModified`, schema FAQ, penulisan ulang meta dengan klaim baru. Kata "blog" di skill berarti artikel WordPress klien.
8. **Fakta:** tidak ada sumber, tidak ditulis. Skill yang menyuruh "mencari statistik pengganti" dijalankan hanya bila sumbernya benar-benar dibaca pada sesi ini.

## Peta: tahap pipeline → skill

Tahap mengikuti `AGENT.md` Section 4. Baca hanya bagian yang dirujuk, tidak perlu seluruh berkas.

| Tahap | Skill (berkas di `skills/pustaka/<nama>/SKILL.md`) | Dipakai untuk | Bagian yang dibaca |
|---|---|---|---|
| 2 Audit draft | `blog-seo-check` | Kerangka validasi on-page: title, meta, heading, link, alt, URL | Step 2–6 dan 10 |
| 2 Audit draft | `blog-rewrite` | Audit read-only sebelum menulis ulang | Phase 1 |
| 2 Audit draft | `blog-cannibalization` | Konsep bentrok keyword antar artikel (mode lokal saja) | Local Mode Workflow |
| 3 Humanize | `antislop-copywriting` | Katalog pola tulisan mesin dan cara memperbaikinya | Seluruhnya (±25 KB) |
| 3 Humanize | `antislop` (inti) | Aturan tulisan: R-02, R-15–R-18, R-36, R-38 | "Copywriting & Content" dan aturan R terkait |
| 3 Humanize | `blog-rewrite` | Metode menulis ulang, jaga suara penulis, larang statistik fiktif | Phase 4 dan 5 |
| 3 Humanize | `blog/references/ai-slop-detection.md` | Pemeriksaan pola berulang dan ritme datar | Seluruhnya (pendek) |
| 4 Verifikasi | `blog-seo-check` | Cek ulang setelah revisi | Step 11 |
| 4 Verifikasi | `blog-factcheck` | Cek sumber yang dikutip artikel | Step 2–5 |
| Opsional | `copy-editing` | Bila operator meminta REVISION atau kalimat terasa kaku | Seven Sweeps |
| Opsional | `copywriting` | Halaman pemasaran klien (bukan artikel) | Writing Style Rules |
| Opsional | `seo-audit` | Audit halaman atau situs klien yang sudah tayang | Sesuai kebutuhan |
| Opsional | `ai-seo` | Optimasi agar dikutip mesin pencari AI | Sesuai kebutuhan |
| Opsional | `schema` | Penanda JSON-LD untuk halaman klien | Sesuai kebutuhan |
| Opsional | `blog-geo` | Skor kesiapan dikutip AI untuk satu artikel | Audit Process |

Rujukan pendukung ada di `blog/references/` (misalnya `quality-scoring.md`, `eeat-signals.md`, `internal-linking.md`). Bagian `blog/SKILL.md` hanya perlu dibuka bila skill lain menunjuk ke sana.

## Cara memanggil dalam sebuah tugas

1. Tentukan tahap yang sedang dikerjakan, lalu cari barisnya di tabel.
2. Baca berkas skill yang disebut, hanya bagian yang tertulis.
3. Terapkan aturan adaptasi di atas bila ada isi skill yang bertentangan.
4. Tetap jalankan `alat/cek-artikel.py`. Hasil skill tidak menggantikan gerbang.

Skill sengaja tidak ditempel semuanya ke chat. Membaca seluruh pustaka (±630 KB) menghabiskan konteks tanpa menambah mutu.

## Sumber dan lisensi

| Folder | Asal | Lisensi |
|---|---|---|
| `blog`, `blog-seo-check`, `blog-rewrite`, `blog-factcheck`, `blog-geo`, `blog-cannibalization` | claude-blog oleh AgriciDaniel | MIT, `LISENSI/claude-blog.MIT.txt` |
| `seo-audit`, `ai-seo`, `schema`, `copywriting`, `copy-editing` | marketingskills oleh Corey Haines | MIT, `LISENSI/marketingskills.MIT.txt` |
| `antislop`, `antislop-copywriting` | anti-slop oleh Miqdad Badjuber | MIT, `LISENSI/anti-slop.MIT.txt` |

Perubahan dari aslinya: berkas `evals/` dibuang, folder `scripts/`, `templates/`, `agents/`, `data/` milik `blog` dibuang, dan akhir baris diseragamkan ke LF. Isi SKILL.md tidak diubah. Teks lisensi diambil dari repo asal pada 2026-11-21.
Untuk memperbarui: ambil versi baru dari repo asal, timpa folder terkait, lalu jalankan `python -I -X utf8 alat/uji-tools.py`.
