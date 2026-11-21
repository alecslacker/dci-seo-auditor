# Aturan Inti (jalur cepat untuk model kecil)

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved

Ini ringkasan satu halaman. Bila ada yang bertentangan, `AGENT.md` Section 11 menang. Buka `AGENT.md` penuh hanya untuk hal yang tidak ada di sini (format ledger, status langka, template HTML persis). Jangan membaca `skills/pustaka/`.

## Urutan kerja (jangan lompat, jangan ulang tahap yang sudah selesai)

1. Status: `python -I -X utf8 alat/cek-status.py "klien/<Klien>/artikel/<YYYY Bulan>"`. Kerjakan hanya `BARU` dan `LANJUTKAN`. Status lain dilaporkan, tidak disentuh.
2. Audit: `python -I -X utf8 alat/cek-artikel.py "<draft>" --draft`. Baca daftar TEMUAN, jangan ubah apa pun.
3. Humanize: tulis `<nama> - Humanized.txt` SEKALI, penuh, sesuai bagian "Cara menulis ulang". Draft asli tidak ditimpa.
4. Meta: tulis `<nama> - Meta.txt` (tiga baris: `Judul SEO:`, `Deskripsi meta:`, `Slug:`).
5. Gerbang: `python -I -X utf8 alat/cek-artikel.py "<artikel Humanized>"`. Perbaiki hanya baris FAIL. Maksimal 2 putaran. Masih FAIL setelah itu: berhenti, lapor sisa FAIL ke operator.
6. ZeroGPT: `python -I -X utf8 alat/siap-zerogpt.py "<artikel Humanized>"`. Operator yang memindai. Salin blok TUGAS OPERATOR ke laporan akhir.
7. Catat ledger (hash disalin dari keluaran `cek-status.py`) dan blok laporan di `LAPORAN.md`.

## Cara menulis ulang (ini yang menentukan skor ZeroGPT)

- Pertahankan kerangka HTML draft (tautan, `<!--more-->`, `<h2>`, `<p>&nbsp;</p>`, blok gambar, kontak, shortcode). Ubah hanya kalimat prosa.
- Per paragraf: tangkap maksudnya dalam satu kalimat, tutup draft, tulis dari maksud itu. Mengganti beberapa kata tidak cukup (FAIL bila lebih dari 25% rangkaian 8 kata draft masih utuh).
- Panjang kalimat berselang: pendek (5-8 kata), sedang (12-18), sesekali panjang (20-30). Dilarang tiga kalimat berurutan dengan panjang sama.
- Panjang paragraf berselang (1-7 kalimat). Dua paragraf berurutan tidak boleh dibuka kata yang sama.
- Pakai pelaku yang jelas dan kalimat aktif. Sebut hal konkret dari `CLIENT.md` atau situs klien. Tidak ada datanya: biarkan umum, jangan mengarang.
- Penanda percakapan ("nah,", "jujur saja,", "sebenarnya,") maksimal 1-2 kali per artikel untuk masing-masing. Satu atau dua pertanyaan retoris cukup.
- Jangan terlalu steril. Sisakan selingan pendapat di antara bagian yang padat detail.

## Larangan mutlak

- Tanda pisah panjang (em dash), rumus "bukan hanya X, tetapi Y", tiga serangkai dipaksakan, rangkaian fragmen pendek beruntun.
- Cliché: "Di era modern ini", "Tidak dapat dipungkiri", "Perlu diketahui bahwa", "Sangat penting untuk", "Merupakan salah satu", "Berbagai macam", "Memainkan peran penting", "Dalam dunia yang semakin berkembang".
- "Anda" berkapital kecuali di awal kalimat. Tulis "silakan", bukan "silahkan". Tidak ada heading "Kesimpulan".
- Kata asing yang punya padanan baku ditulis ulang (snack box jadi kotak kudapan, dessert jadi pencuci mulut). Pertahankan nama brand, keyword, dan istilah di `CLIENT.md`.
- Mengarang statistik, testimoni, nama, penghargaan, tahun pengalaman, atau harga pasti. Harga hanya "kisaran" atau "tergantung".
- Menyebut atau menautkan klien lain.

## Angka yang diperiksa gerbang

Paragraf pertama minimal 200 kata. Keyword 31-34 kali (density 1,0-2,5%), di body tebal dan Title Case, di heading Title Case tanpa `<b>`, dan ada di sedikitnya dua `<h2>`. Satu penanda `<b>INI BAGIAN INBOUND LINK</b>` di paragraf 2-5. Minimal satu daftar. Shortcode WA hanya di baris terakhir.

## Batas kerja

- Tulis berkas hasil sekali. Setelah FAIL, edit bagian yang gagal, jangan tulis ulang seluruh artikel.
- Jangan menyatakan lulus tanpa `0 FAIL` dari gerbang terbaru pada berkas terbaru.
- Angka ZeroGPT hanya dari laporan operator. Belum ada: tulis `MENUNGGU OPERATOR`.
