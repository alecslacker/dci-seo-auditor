# DCI SEO Auditor: Agentic SEO Auditor by Duta Corpora Indonesia

DCI SEO Auditor mengubah draft artikel mentah dari plugin AI Puffer menjadi artikel WordPress yang siap tayang. Agent mengerjakan audit, penulisan ulang, dan pemeriksaan. Dua skrip Python menjadi gerbang yang memutuskan lulus atau tidaknya, jadi hasilnya tidak bergantung pada penilaian agent sendiri.

Tool ini dibuat untuk karyawan Duta Corpora Indonesia. Cara agent menyapa operator mengikuti `AGENTS.md` atau persona di komputer masing-masing.

Target tiap artikel: skor Rank Math 80 sampai 100, bahasa Indonesia baku, lolos ZeroGPT, dan tercatat per klien.

```text
draft mentah ──► GERBANG STATUS ──► AUDIT ──► ZeroGPT DRAF ──┬─ di bawah 10% ──► perbaiki temuan ──┐
                                                            └─ 10% atau lebih ─► HUMANIZE ──► ZeroGPT final
                                                                                                  │
              GERBANG KUALITAS ◄──────────────────────────────────────────────────────────────────┘ ──► LAPORAN
              (perbaiki hanya bagian FAIL)
```

## Mulai cepat di Windows

1. Pastikan Python sudah terpasang (bila belum, `MULAI.bat` akan menunjukkan caranya).
2. Klik dua kali **`MULAI.bat`** di folder utama project.
3. Pilih pekerjaan dengan mengetik angka lalu Enter. Semua petunjuk berbahasa Indonesia.

| Menu | Gunanya |
|---|---|
| 1. Siapkan komputer | Memasang perintah `/artikel` ke program AI Anda (sekali saja) |
| 2. Salin perintah kerja | Menyiapkan perintah untuk ditempel ke program AI, otomatis masuk clipboard |
| 3. Lihat status draft | Menunjukkan draft mana yang sudah, belum, atau menunggu dikerjakan |
| 4. Periksa artikel | Menyatakan LULUS atau BELUM LULUS beserta daftar yang harus diperbaiki |
| 5. Tambah klien baru | Membuat folder klien dari template dan membuka `CLIENT.md` untuk diisi |
| 6. Bantuan | Urutan kerja singkat |

Menu hanya mengatur berkas dan menjalankan pemeriksaan. Penulisan ulang artikelnya tetap dikerjakan program AI Anda (TRAE, ZCode, Claude Code, dan sejenisnya) dengan perintah yang disalin dari menu 2.

## Yang dijamin dan yang tidak

Gerbang kualitas membuktikan bahwa artikel memenuhi aturan format dan bahasa di repo ini: jumlah kata, keyword, heading, format WordPress, judul SEO dan slug, ejaan, serta tidak ada kalimat yang disalin dari artikel lain. Lulus berarti `0 FAIL`.

Gerbang tidak menjamin peringkat. Skor Rank Math adalah skor plugin, bukan sinyal Google. Google tidak menetapkan jumlah kata atau jumlah keyword, dan melarang pengulangan yang terdengar tidak wajar (`FAKTA-SEO.md`). Target 31 sampai 34 kali keyword adalah aturan template kita sendiri. Hasil di Google hanya bisa dinilai dari data Search Console klien.

## Cara kerja

1. **Gerbang status.** `cek-status.py` membandingkan sidik jari isi draft dengan ledger di `LAPORAN.md`. Draft yang sudah diaudit tidak diaudit dua kali, dan draft yang masih ditulis penulis dilewati.
2. **Audit.** `cek-artikel.py --draft` mengeluarkan daftar temuan bernomor: komponen wajib, ejaan tidak baku, kata asing, angka tanpa label, dan pola khas tulisan AI. Audit ini tidak pernah menghentikan pekerjaan (exit 0).
3. **ZeroGPT draf, lalu humanize bila perlu.** Operator memindai DRAF dulu. Di bawah 10% AI, humanize dilewati dan agent hanya memperbaiki temuan audit (gerbang dijalankan dengan `--tanpa-humanize`). Di atas atau sama dengan 10%, agent menulis ulang. Ambang ini baru berdasar satu artikel uji, jadi skor draf dan final dicatat untuk dievaluasi. Agent menulis ulang berdasarkan daftar temuan dan `aturan/INTI.md` (ringkasan satu halaman; rincian di `aturan/kerja-tanpa-skill.md`). Statistik, testimoni, dan nama tidak boleh dikarang.
4. **Gerbang kualitas.** `cek-artikel.py` memeriksa artikel. Artikel lulus bila hasilnya `0 FAIL`. Judul SEO, deskripsi meta, dan slug tidak dikerjakan agent karena dibuat otomatis oleh AIPuffer di WordPress.
5. **ZeroGPT dan laporan.** Operator memindai payload (disiapkan agent lewat `alat/siap-zerogpt.py`) di ZeroGPT, lalu angkanya dicatat apa adanya di `LAPORAN.md` klien.

### Status draft

| Status | Artinya |
|---|---|
| `BARU` | Draft lengkap, belum pernah diaudit |
| `MENUNGGU` | Draft belum lengkap, penulis masih bekerja |
| `LANJUTKAN` | Pernah dikerjakan sebagian, hanya tahap yang kosong dilanjutkan |
| `SELESAI` | Semua tahap tercatat, tidak diaudit ulang |
| `BERUBAH` | Draft diedit setelah diaudit, agent bertanya ke operator |
| `TANPA-CATATAN` | Versi Humanized ada tetapi tidak tercatat di ledger |
| `RUSAK` | Berkas bukan UTF-8, perlu disimpan ulang |

### Kode keluar `cek-artikel.py`

| Kode | Artinya |
|---|---|
| `0` | Tidak ada FAIL |
| `1` | Ada FAIL: perbaiki bagian yang gagal |
| `2` | Masukan tidak bisa diperiksa: berkas tidak ada, bukan UTF-8, keyword tidak terdeteksi, atau `CLIENT.md` belum diisi |

## Skill SEO dan audit di dalam repo

Karyawan tidak perlu memasang skill. Tiga belas skill SEO dan audit (claude-blog, marketingskills, anti-slop; semuanya MIT) ada di `skills/pustaka/`, sudah disunting agar berdiri sendiri (tanpa plan mode, skrip, atau alat berbayar). Agent membacanya lewat jalur berkas, jadi sama di TRAE, ZCode, Claude Code, Codex, dan agent lain. `skills/pustaka/INDEKS.md` memetakan tiap tahap pipeline ke skill yang harus dibaca, ditambah aturan adaptasi (misalnya tanpa plan mode dan tanpa alat berbayar) yang mengalahkan isi skill. Gerbang kelulusan tetap `alat/cek-artikel.py` dengan 0 FAIL.

## Struktur

```text
.
├── AGENTS.md                # penunjuk pendek (±500 token) yang dimuat agent otomatis
├── AGENT.md                 # aturan kerja: pipeline, checklist, protokol, template prompt
├── FAKTA-SEO.md             # fakta Google dan Rank Math, lengkap sumber dan tanggal
├── aturan/
│   ├── INTI.md              # ringkasan satu halaman untuk model kecil (jalur cepat)
│   └── kerja-tanpa-skill.md # aturan kerja mandiri, tidak butuh skill terpasang
├── PROMPT PINTASAN.md       # panduan /artikel, isi perintah, cara memasang, prompt cadangan
├── CHANGELOG.txt            # riwayat perubahan sistem
├── CLAUDE.md                # impor AGENTS.md untuk Claude Code
├── MULAI.bat                # klik dua kali: membuka menu berbahasa Indonesia (Windows)
├── perintah/
│   └── artikel.md           # sumber netral command /artikel (tanpa format khusus agent)
├── skills/
│   ├── dci-seo-auditor/     # skill penunjuk ke aturan repo (dipasang pasang-perintah.py)
│   ├── research-guide/      # protokol riset milik DCI (dipasang pasang-perintah.py)
│   └── pustaka/             # 13 skill SEO dan audit (MIT) + INDEKS.md + LISENSI/, dibaca lewat jalur
├── alat/
│   ├── menu.py              # menu interaktif yang dibuka MULAI.bat
│   ├── cek-status.py        # gerbang status draft
│   ├── cek-artikel.py       # audit draft dan gerbang kualitas final
│   ├── siap-zerogpt.py      # siapkan payload ZeroGPT untuk operator (Section 6 AGENT.md)
│   ├── cek-ai-api.py        # EKSPERIMENTAL: skor AI per kalimat lewat Winston (kunci dari env, belum dikalibrasi)
│   ├── pasang-perintah.py   # memasang /artikel ke TRAE, ZCode, atau Claude Code
│   ├── kamus-id.txt         # kata dasar bahasa Indonesia (hunspell-id, LGPL-3.0) untuk cek salah ketik
│   ├── kamus-id.LICENSE.txt # teks lisensi LGPL-3.0 kamus di atas
│   ├── kamus-kata.txt       # tambahan manual: nama, istilah, kata hasil tinjauan
│   └── uji-tools.py         # uji otomatis semua skrip
└── klien/                   # semua data klien ada di sini
    ├── _TEMPLATE/           # cetakan klien baru
    └── <Nama Klien>/
        ├── CLIENT.md        # data klien
        └── artikel/<YYYY Bulan>/
            ├── <slug>.txt              # draft mentah (arsip, tidak ditimpa)
            ├── <slug> - Humanized.txt  # hasil akhir, siap tempel ke WordPress
            └── LAPORAN.md              # ledger dan laporan bulan itu
```

Folder berawalan `_` bukan klien dan tidak pernah diproses. Folder milik agent (`.trae/`, `.zcode/`, `.claude/`, `.agents/`, dan sejenisnya) ada di `.gitignore` dan tidak ikut repo. Semua yang dibutuhkan pipeline ada di `alat/`, `aturan/`, `perintah/`, dan `klien/`, sehingga bekerja di agent mana pun.

## Memulai

Butuh agent apa pun yang bisa membaca berkas biasa (TRAE, ZCode, Claude Code, Codex, dan lainnya) dan Python 3.8 ke atas. Tidak perlu memasang skill: semua aturan ada di repo ini (`aturan/kerja-tanpa-skill.md`). Di Windows, jalankan skrip dengan `python`. Contoh di dokumen memakai `python3`.

1. **Daftarkan klien.** Salin `klien/_TEMPLATE/` menjadi `klien/<Nama Klien>/`, ganti nama folder `YYYY Bulan` menjadi bulan kerja, lalu isi semua field di `CLIENT.md`. Isian bawaan template yang belum diganti ditolak skrip.
2. **Taruh draft.** Simpan draft mentah dari AI Puffer di `klien/<Nama Klien>/artikel/<YYYY Bulan>/<judul>.txt`.
3. **Pasang perintah** (sekali per komputer, hanya bila ingin memakai `/artikel`): `python -I -X utf8 alat/pasang-perintah.py trae` (atau `zcode`, `claude`, `semua`). Berkas command tidak ikut repo karena tiap agent punya format sendiri. Rinciannya di `PROMPT PINTASAN.md`.
4. **Jalankan** dengan root project sebagai workspace.
   - Dengan command: `/artikel Salimah Catering November`. Untuk TRAE, pastikan opsi *Include AGENTS.md in the context* aktif di Settings > Rules & Memories.
   - Agent mana pun, tanpa command: `Baca AGENT.md, lalu kerjakan Salimah Catering bulan November sesuai Section 10.`
5. **Ambil hasil.** `<judul> - Humanized.txt` siap ditempel ke editor WordPress. `LAPORAN.md` memuat metrik, angka ZeroGPT, dan catatan risiko. Judul SEO, deskripsi meta, dan permalink diisi AIPuffer di WordPress.

## Alat bawaan

| Perintah | Fungsi |
|---|---|
| `python3 -I alat/cek-status.py "klien/<klien>/artikel/<bulan>"` | Klasifikasi draft sebelum dikerjakan |
| `python3 -I -X utf8 alat/cek-artikel.py "<draft>" --draft` | Audit draft mentah, keluar daftar temuan |
| `python3 -I -X utf8 alat/cek-artikel.py "<artikel>"` | Gerbang kualitas final, exit 1 bila ada FAIL |
| `python3 -I -X utf8 alat/pasang-perintah.py trae` | Pasang `/artikel` ke TRAE. Lainnya: `zcode`, `claude`, `semua`, `--daftar`, `--cek` |
| `python3 -X utf8 alat/menu.py` | Membuka menu tanpa MULAI.bat (macOS, Linux, atau terminal) |
| `python3 -I -X utf8 alat/uji-tools.py` | Uji otomatis semua skrip (194 uji). Jalankan setelah mengubah skrip |
| `python3 -I -X utf8 alat/cek-artikel.py "<artikel>" --tanpa-humanize` | Gerbang final untuk artikel dari draf yang lolos ZeroGPT di bawah 10% (melewati ukuran parafrase saja) |
| `python3 -I -X utf8 alat/siap-zerogpt.py "<draf atau Humanized>" ["<lain>" ...]` | Siapkan `payload-zerogpt.txt` (satu atau banyak berkas) untuk operator pindai di ZeroGPT |
| `WINSTON_API_KEY=<kunci> python3 -I -X utf8 alat/cek-ai-api.py "<artikel Humanized>" --ambang 50` | EKSPERIMENTAL. Tulis `kalimat-ai.txt` (skor manusia Winston per kalimat). Bukan pengganti ZeroGPT. Di PowerShell: `$env:WINSTON_API_KEY="<kunci>"` dulu |

Cek ejaan berjalan offline, tanpa kuota dan tanpa internet. Kata di luar kamus (`kamus-id.txt` ditambah `kamus-kata.txt`, dengan pengupasan imbuhan sederhana) menjadi FAIL di gerbang final, dan hanya temuan di mode `--draft`. Ejaan tidak baku, kata asing, kata cakapan (nggak, udah, aja), dan kata kembar (di di) juga FAIL. Kamus tidak memuat kosakata terbaru, jadi nama, istilah, atau kata baru yang sah ditambahkan ke `kamus-kata.txt` (satu kata per baris, huruf kecil). Skrip tidak lagi memakai KBBI Daring karena kuota hariannya dan ketentuan hak ciptanya tidak cocok untuk pemakaian massal.

## ZeroGPT

Pemindaian dikerjakan oleh operator (manusia), bukan agent (keputusan 2026-11-21). Agent hanya menyiapkan payload: `python3 -I -X utf8 alat/siap-zerogpt.py "<artikel Humanized>"` menghasilkan `payload-zerogpt.txt` di folder artikel — HTML dan shortcode sudah dibuang, teks dipecah di batas 15.000 karakter (batas gratis ZeroGPT). Operator menempel tiap bagian ke <https://www.zerogpt.com/> dan melaporkan hasilnya; agent mencatat angka apa adanya ke `LAPORAN.md` (target verdict *Human written*, AI di bawah 10%). Bila belum dipindai, kolom ZeroGPT diisi `MENUNGGU OPERATOR`. Plagiarisme belum punya alat cek otomatis. Gerbang kualitas hanya menangkap kalimat yang disalin antar artikel di repo ini.

## Contoh

Artikel *Jasa Catering Instansi Blitar* milik Salimah Catering: 2.073 kata, keyword 31 kali (density 1,50%), gerbang `0 FAIL 0 WARN`. Angka ZeroGPT (AI 3,7%, *Human written*) berasal dari catatan di `LAPORAN.md` dan belum diverifikasi ulang. Rinciannya ada di `klien/Salimah Catering/artikel/2026 November/LAPORAN.md`.

## Batasan yang diketahui

- `/artikel` belum diuji dari menu TRAE. Formatnya meniru command TRAE yang sudah ada.
- Opsi *Include AGENTS.md in the context* di TRAE adalah pengaturan per komputer, tidak bisa dibagikan lewat repo.
- Ambang kalimat yang disalin (3 rangkaian 8 kata) belum dikalibrasi pada artikel nyata lebih dari satu klien.
- Ambang kedalaman parafrase (FAIL di atas 25% rangkaian 8 kata draft yang masih utuh) baru dikalibrasi pada satu artikel lulus (2,8%) dan dua tulisan ulang dangkal (79-82%).
- Uji A/B sah pada 2026-11-21 (dengan parafrase penuh): hasil dengan dan tanpa pustaka sama di semua metrik (gerbang, ritme, ZeroGPT). Pustaka kini rujukan opsional, bukan langkah pipeline.
- Kamus offline berasal dari KBBI edisi 3 (lewat hunspell-id), jadi kosakata terbaru dan nama diri bisa muncul sebagai FAIL yang sebenarnya sah. Operator menambahkannya ke `alat/kamus-kata.txt` setelah memastikan ejaannya benar.
- Salah ketik yang kebetulan membentuk kata sah tidak tertangkap (misalnya "pesana" dibaca pe+sana, atau "makan" yang seharusnya "makanan").

---

Author: Mas Wondho — Duta Corpora Indonesia (DCI)
Copyright © 2026 Duta Corpora Indonesia — All rights reserved
