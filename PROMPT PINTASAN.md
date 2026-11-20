# PINTASAN — DCI SEO Auditor

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved

## Cara utama: command `/artikel`

Ketik di kotak input TRAE (ketik `/` lalu pilih `artikel`):

```
/artikel <nama perusahaan> <bulan> [tahun]
```

Contoh:

```
/artikel Salimah Catering November
/artikel Salimah Catering November 2026
```

Aturan membaca: kata terakhir = bulan (atau kata sebelum angka tahun), semua kata di depannya = nama perusahaan. Nama perusahaan boleh lebih dari satu kata.

File command: `.trae/commands/artikel.md` (di ROOT project ini). Command menyuruh agent memuat 4 skill (antislop-copywriting, blog-rewrite, blog-seo-check, verification-before-completion) dan membaca `AGENT.md` Section 10.

### Syarat agar `/artikel` muncul di menu `/`

- TRAE harus dibuka dengan **ROOT project ini sebagai workspace** (folder yang berisi `AGENT.md` dan `.trae/`). Command project dibaca dari `.trae/commands` (dokumentasi TRAE: docs.trae.ai/ide/slash-commands).
- Bila tidak muncul, buka Settings > Skills & Commands dan cek bagian Commands, atau buka sesi baru.
- Bila ingin command ini tersedia di semua project, salin `artikel.md` ke `%userprofile%/.trae/commands`. Konsekuensinya, command itu mengandalkan `AGENT.md` di folder kerja saat dipanggil, jadi hanya berguna bila ROOT ini yang sedang dibuka.

## Cadangan: prompt biasa (tanpa command)

```
@AGENT.md Kerjakan [NAMA PERUSAHAAN] bulan [NAMA BULAN] sesuai Section 10 (Mode Pintasan).
```

TRAE membaca `AGENTS.md` (pakai S) dan `CLAUDE.md` bila opsinya diaktifkan di Settings > Rules & Memories. `AGENTS.md` di repo ini sengaja pendek dan hanya menunjuk ke `AGENT.md` (aturan lengkap, ±8.000 token), jadi `AGENT.md` tidak termuat sendiri. Karena itu prompt cadangan memakai `@AGENT.md`.

## Yang terjadi setelah dikirim

1. Agent mencari folder perusahaan dan membaca `CLIENT.md`-nya.
2. Mencari folder bulan di `artikel/`, lalu menjalankan Gerbang Status pada semua draft.
3. Hanya draft `BARU` dan `LANJUTKAN` yang dikerjakan: audit, humanize, verifikasi script, lalu scan ZeroGPT.
4. Hasil: `<judul> - Humanized.txt` per artikel, serta ledger dan laporan di `LAPORAN.md` folder bulan itu.
5. Laporan ringkas di chat, termasuk draft yang dilewati beserta alasannya.

## Kalau penulis mengerjakan bertahap

Aman dijalankan berulang kali. Gerbang Status membandingkan isi draft dengan ledger di `LAPORAN.md`:

| Status | Artinya | Yang dilakukan agent |
|---|---|---|
| `BARU` | Draft lengkap, belum pernah diaudit | Audit penuh |
| `MENUNGGU` | Draft belum lengkap (belum berakhir dengan shortcode WA klien) | Dilewati |
| `LANJUTKAN` | Pernah dikerjakan sebagian | Hanya tahap yang masih kosong |
| `SELESAI` | Semua tahap sudah tercatat | Dilewati, tidak diaudit ulang |
| `BERUBAH` | Penulis mengedit draft setelah diaudit | Berhenti dan bertanya ke operator |
| `TANPA-CATATAN` | Versi Humanized ada tetapi tidak tercatat di ledger | Dilewati dan dilaporkan |

Untuk memaksa audit ulang, tulis di akhir perintah: `Audit ulang [nama draft], alasannya: ...`.

## Syarat sebelum dipakai untuk klien baru

- Folder klien ada di `klien/` (salin dari `klien/_TEMPLATE/`) dan `CLIENT.md`-nya terisi lengkap (lihat `AGENT.md` Section 3).
- Draft mentah `.txt` ada di `klien/<Klien>/artikel/<tahun bulan>/`.
- Agent punya akses browser (untuk ZeroGPT). Bila gagal, agent menandai `MANUAL CHECK NEEDED`.

## Variasi opsional (tambahkan di akhir perintah)

- `Hanya audit, jangan humanize.` untuk melihat temuan saja.
- `Hanya file [nama draft].` untuk satu artikel.
- `Lewati ZeroGPT.` bila hanya butuh rewrite.
