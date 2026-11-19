# PINTASAN — Artikel AI Puffer

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved

## Cara utama: command `/artikel`

Ketik di kotak input ZCode:

```
/artikel <nama perusahaan> <bulan> [tahun]
```

Contoh:

```
/artikel Salimah Catering November
/artikel Salimah Catering November 2026
```

Aturan membaca: kata terakhir = bulan (atau kata sebelum angka tahun), semua kata di depannya = nama perusahaan. Nama perusahaan boleh lebih dari satu kata.

File command: `.zcode/commands/artikel.md` (di ROOT project ini). Command memuat otomatis 4 skill (antislop-copywriting, blog-rewrite, blog-seo-check, verification-before-completion) dan menyuruh agent membaca `AGENT.md` Section 10.

### Syarat agar `/artikel` muncul di menu `/`

- ZCode harus dibuka dengan **ROOT project ini sebagai workspace** (folder yang berisi `AGENT.md` dan `.zcode/`). Command workspace hanya dipindai dari folder kerja ke atas sampai root repositori.
- Bila tidak muncul setelah file dibuat, muat ulang jendela ZCode atau buka sesi baru.
- Bila ingin command ini tersedia di semua workspace, salin `artikel.md` ke `~/.zcode/commands/`. Konsekuensinya, command itu mengandalkan `AGENT.md` di folder kerja saat dipanggil, jadi hanya berguna bila ROOT ini yang sedang dibuka.

## Cadangan: prompt biasa (tanpa command)

```
@AGENT.md Kerjakan [NAMA PERUSAHAAN] bulan [NAMA BULAN] sesuai Section 10 (Mode Pintasan).
```

ZCode hanya membaca `AGENTS.md` (pakai S) secara otomatis, sedangkan file ini bernama `AGENT.md`, jadi tidak termuat sendiri. Karena itu prompt cadangan memakai `@AGENT.md`.

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
| `BERUBAH` | Penulis mengedit draft setelah diaudit | Berhenti dan bertanya ke Mas Ulum |
| `TANPA-CATATAN` | Versi Humanized ada tetapi tidak tercatat di ledger | Dilewati dan dilaporkan |

Untuk memaksa audit ulang, tulis di akhir perintah: `Audit ulang [nama draft], alasannya: ...`.

## Syarat sebelum dipakai untuk klien baru

- Folder klien ada di ROOT dan berisi `CLIENT.md` yang terisi lengkap (template di `AGENT.md` Section 3).
- Draft mentah `.txt` ada di `<Klien>/artikel/<tahun bulan>/`.
- Browser dalam aplikasi ZCode bisa dibuka (untuk ZeroGPT). Bila gagal, agent menandai `MANUAL CHECK NEEDED`.

## Variasi opsional (tambahkan di akhir perintah)

- `Hanya audit, jangan humanize.` untuk melihat temuan saja.
- `Hanya file [nama draft].` untuk satu artikel.
- `Lewati ZeroGPT.` bila hanya butuh rewrite.
