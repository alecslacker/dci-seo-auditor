# Aturan Inti (jalur cepat untuk model kecil)

> Author: Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved

Ini ringkasan satu halaman. Bila ada yang bertentangan, `AGENT.md` Section 11 menang. Buka `AGENT.md` penuh hanya untuk hal yang tidak ada di sini (format ledger, status langka, template HTML persis). Jangan membaca `skills/pustaka/`.

## Urutan kerja (jangan lompat, jangan ulang tahap yang sudah selesai)

1. Status: `python -I -X utf8 alat/cek-status.py "klien/<Klien>/artikel/<YYYY Bulan>"`. Kerjakan hanya `BARU` dan `LANJUTKAN`. Status lain dilaporkan, tidak disentuh.
2. Audit: `python -I -X utf8 alat/cek-artikel.py "<draft>" --draft`. Baca daftar TEMUAN, jangan ubah apa pun.
3. ZeroGPT DRAF dulu (berlaku semua klien): `python -I -X utf8 alat/siap-zerogpt.py "<draft 1>" "<draft 2>" ...` (boleh banyak draft sekaligus). Catat ledger (Audit terisi, Humanize `-`, ZeroGPT `MENUNGGU OPERATOR (draf)`), salin blok TUGAS OPERATOR, lalu BERHENTI dan lapor. Jangan humanize sebelum operator melapor skor draf.
4. Keputusan per draft dari skor operator: di bawah 10% = lewati humanize (langkah 4a). 10% atau lebih = humanize penuh (langkah 4b). Operator belum atau tidak bisa melapor: humanize penuh seperti biasa.
   - 4a. Salin draft jadi `<nama> - Humanized.txt`, perbaiki HANYA temuan audit (em dash, "Anda" kapital, kata asing, ejaan, struktur WP). Jangan menulis ulang kalimat lain.
   - 4b. Tulis `<nama> - Humanized.txt` SEKALI, penuh, sesuai bagian "Cara menulis ulang". Draft asli tidak ditimpa.
5. Tidak membuat berkas meta. Judul SEO, deskripsi meta, dan slug dibuat AIPuffer di WordPress. Jangan menulis `- Meta.txt`.
6. Gerbang: `python -I -X utf8 alat/cek-artikel.py "<artikel Humanized>"` (jalur 4a tambah `--tanpa-humanize`). Perbaiki semua baris FAIL sekaligus dalam satu kali edit, lalu jalankan ulang. Maksimal 2 putaran. Masih FAIL setelah itu: berhenti, lapor sisa FAIL ke operator.
   - Ejaan dicek SEKALI, di sini, bukan saat menulis. Selesai tulis, jangan baca ulang. Lihat baris WARN "kata di luar kamus": perbaiki yang salah ketik dalam edit yang sama dengan perbaikan FAIL, biarkan kata serapan atau istilah yang sah. WARN tidak membuat putaran baru.
7. ZeroGPT FINAL: hanya jalur 4b (`siap-zerogpt.py "<artikel Humanized>"`; kolom ZeroGPT diganti `MENUNGGU OPERATOR (final)` sampai operator melapor). Jalur 4a: catat skor draf di kolom ZeroGPT dengan tambahan `(draf)`, operator boleh memindai ulang bila ingin. Salin blok TUGAS OPERATOR bila ada yang menunggu.
8. Catat ledger (hash disalin dari keluaran `cek-status.py`; jalur 4a: Humanize `dilewati (draf <10%)`) dan blok laporan di `LAPORAN.md`.

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
- Kata cakapan (nggak, udah, aja, banget) dan kata kembar (di di): FAIL. Kata di luar kamus hanya WARN satu baris: lihat sekali, perbaiki bila salah ketik, biarkan kata serapan atau istilah yang sah.
- Mengarang statistik, testimoni, nama, penghargaan, tahun pengalaman, atau harga pasti. Harga hanya "kisaran" atau "tergantung".
- Menyebut atau menautkan klien lain.

## Angka yang diperiksa gerbang

Paragraf pertama minimal 200 kata. Keyword 31-34 kali (density 1,0-2,5%), di body tebal dan Title Case, di heading Title Case tanpa `<b>`, dan ada di sedikitnya dua `<h2>`. Satu penanda `<b>INI BAGIAN INBOUND LINK</b>` di paragraf 2-5. Minimal satu daftar. Shortcode WA hanya di baris terakhir.

## Batas kerja

- Tulis berkas hasil sekali. Setelah FAIL, edit bagian yang gagal, jangan tulis ulang seluruh artikel.
- Kerja cepat, tanpa berputar: tulis sekali, jalankan gerbang, perbaiki semua yang dilaporkan dalam satu edit, selesai. Jangan memeriksa ejaan atau membaca ulang artikel sebelum gerbang; skrip memeriksa semua kata. Protokol anti-typo untuk kode tidak berlaku pada isi artikel.
- Jangan menyatakan lulus tanpa `0 FAIL` dari gerbang terbaru pada berkas terbaru.
- Angka ZeroGPT hanya dari laporan operator. Belum ada: tulis `MENUNGGU OPERATOR`.
- Ambang 10% adalah target praktis dari satu artikel uji (draf 3,72%, final 3,7%). Catat skor draf dan final di `LAPORAN.md` agar aturan ini bisa dievaluasi.
