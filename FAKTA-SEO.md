# FAKTA-SEO.md — Fakta Google Search & Rank Math (bersumber + tanggal)

> Author: Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved
> Tujuan: satu-satunya tempat klaim "aturan Google/SEO" di project ini. Semua poin diambil langsung
> dari halaman resmi (bukan ingatan), dengan tanggal "Last updated" yang tertera di halaman.
> Fakta bisa berubah: periksa ulang tiap ±3 bulan atau sebelum putaran artikel besar.

## Google Search Central (dokumen resmi)

| Fakta | Sumber (tanggal "Last updated" halaman) |
|---|---|
| Google tidak menetapkan jumlah kata ideal: "Are you writing to a particular word count because you've heard or read that Google has a preferred word count? (No, we don't.)" | Creating helpful, reliable, people-first content — developers.google.com/search/docs/fundamentals/creating-helpful-content (2026-10-05) |
| Definisi keyword stuffing: "Repeating the same words or phrases so often that it sounds unnatural" serta "Blocks of text that list cities and regions that a web page is trying to rank for" | Spam policies — developers.google.com/search/docs/essentials/spam-policies (2026-08-28) |
| Scaled content abuse: "many pages are generated for the primary purpose of manipulating search rankings and not helping users… no matter how it's created" — termasuk "Using generative AI tools… to generate many pages without adding value" | Spam policies (2026-08-28) |
| Konten AI diperbolehkan tetapi wajib diperiksa manusia: "It is critical to manually factcheck and review all AI-generated content… This review also applies to metadata like <title> elements, meta description elements, structured data, and alternate texts for images" | Google Search's guidance on using generative AI content (2026-10-01) |
| Alt text: gunakan deskripsi berguna yang kaya informasi; "Avoid filling alt attributes with keywords (keyword stuffing)". Contoh terbaik: alt yang mendeskripsikan gambar, bukan daftar kata | Google Image best practices — developers.google.com/search/docs/appearance/google-images (2026-03-02) |
| Meta description: "There's no limit on how long a meta description can be, but the snippet is truncated… typically to fit the device width" | Control your snippet — developers.google.com/search/docs/appearance/snippet (2026-04-20) |
| Anchor text harus deskriptif dan berada di elemen `<a href>` yang bisa dirayapi; gunakan nofollow hanya bila tidak percaya sumber | Links crawlable — developers.google.com/search/docs/crawling-indexing/links-crawlable (2025-12-10) |
| E-E-A-T bukan faktor ranking tunggal; sistem memberi bobot lebih pada topik YMYL | Creating helpful content (2026-10-05) |
| Google sarankan byline/penulis jelas serta keterbukaan soal penggunaan AI/otomasi ("Is the use of automation… self-evident to visitors through disclosures?") | Creating helpful content (2026-10-05) |
| November 2026 core update: mulai 2026-11-10, global semua bahasa, rollout bisa sampai 2 minggu | Google Search Status Dashboard — status.search.google.com (feed.atom, diakses 2026-11-20) |

## Rank Math (dokumen plugin, bukan Google)

| Fakta | Sumber |
|---|---|
| Uji Keyword Density: skor penuh bila density 1–1,5%; lebih dari 2,5% kena peringatan; "A low keyword density is better than a high keyword density" | rankmath.com/kb/score-100-in-tests (diakses 2026-11-20) |
| Uji Content Length: 100% hanya di ≥2500 kata; 2000–2500 kata = 70% skor uji itu | rankmath.com/kb/score-100-in-tests (diakses 2026-11-20) |
| Meta description: keyword sebaiknya muncul di 120–160 karakter pertama; SEO title ditampilkan ±60 karakter desktop / ±50 mobile | rankmath.com/kb/score-100-in-tests (diakses 2026-11-20) |

## Konsekuensi untuk pipeline kita

1. Target 2000 kata dan rentang keyword 31–34× adalah **aturan kita sendiri** (template AI Puffer), bukan aturan Google. Google hanya melarang pengulangan yang "sounds unnatural".
2. Density 31×/±2100 kata ≈ 1,4–1,5% — pas dengan band skor penuh Rank Math. Jaga jumlah kata jangan turun, karena density bisa naik melewati 1,5%.
3. Alt text harus deskriptif (keyword + deskripsi gambar), bukan keyword saja.
4. Semua angka harga, klaim kota, dan nama menu wajib dicek ke situs klien/sumber nyata sebelum tayang (kewajiban fact-check Google untuk konten AI).
5. Artikel antar klien dilarang menyalin kalimat satu sama lain: mass-produce tanpa nilai tambah = definisi scaled content abuse.
