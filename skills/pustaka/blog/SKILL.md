---
name: blog
description: >
  Reference pack for the blog skills in this pustaka: quality scoring, E-E-A-T
  signals, internal linking, editorial pattern review, and citation discipline.
  Read a specific reference file when another skill points here; do not load
  the whole pack.
license: MIT
---

<!-- Salinan DCI SEO Auditor, ditulis ulang dari claude-blog (MIT, AgriciDaniel).
     Berkas asli adalah orkestrator 31 sub-skill dengan skrip, subagent, dan
     templates yang tidak disertakan di sini; isinya yang relevan (6 Pillars,
     Quality Gates, daftar references) dipertahankan. Asli: git 746d263. -->

# Blog References (adaptasi DCI)

Folder ini sumber rujukan bagi skill `blog-*` di pustaka. Tidak ada perintah
atau skrip; agent cukup membaca berkas yang ditunjuk.

## Core Methodology: The 6 Pillars

| Pillar | Impact | Implementation |
|--------|--------|---------------|
| Purpose-First Clarity | Reader and retrieval utility | Important sections state their point clearly; no prescribed heading form or passage length |
| Real Sourced Data | E-E-A-T trust | Tier 1-3 sources only, inline attribution |
| Content Structure | Comprehension and reuse | Proper heading hierarchy, stable entities, useful tables/lists only where they fit |
| Substantive Maintenance | Accuracy over date churn | Update content and dateModified only when facts, methods, or recommendations materially change; changing dates to look fresh is a Google warning sign (helpful-content page, updated 2026-10-05) |

(Visual media dan Q&A tidak dipakai di pipeline DCI: keputusan visual milik
operator, dan artikel klien memakai struktur template Section 11.)

## Quality Gates

These are hard rules. Never ship content that violates them:

| Rule | Threshold | Action |
|------|-----------|--------|
| Fabricated statistics | Zero tolerance | Source material factual statistics, measurements, and public-data claims. Dates, step counts, software versions, and prices already attributable or visible in a cited primary source do not need redundant inline sourcing merely because they contain a number |
| Paragraph pacing | Fit the audience and material | Split only when comprehension improves |
| Heading hierarchy | Never skip levels | H1 → H2 → H3 only |
| Source tier | Tier 1-3 only | Never cite content mills or affiliate sites |
| Self-promotion | Max 1 brand mention | Author bio context only |

Di DCI SEO Auditor, gerbang yang mengikat tetap `alat/cek-artikel.py` (`0 FAIL`).

## Anti-Patterns (Never Do These)

| Anti-Pattern | Why |
|-------------|-----|
| Fabricate statistics | May 2026 Core Update and 2026 spam systems reward verifiable trust, not invented claims |
| Keyword-stuff headings or meta | Google ignores/penalizes this |
| Bury important answers | Readers may miss the page's main value |
| Skip source verification | Broken links and wrong data destroy trust |
| Use tier 4-5 sources | Low authority hurts E-E-A-T |
| Generate low-value variations without research | Scaled, interchangeable pages fail the reader-value and evidence requirements |

## References

| Berkas | Isi |
|---|---|
| `references/quality-scoring.md` | Rubrik 100 poin (Content 30, SEO 25, E-E-A-T 15, Technical 15, AI Citation 15) |
| `references/eeat-signals.md` | Penanda experience, expertise, authority, trust |
| `references/internal-linking.md` | Strategi tautan internal dan teks jangkar |
| `references/ai-slop-detection.md` | Pemeriksaan pola berulang orde pertama dan kedua (advisory) |
| `references/research-quality.md` | Rubrik mutu riset, jebakan kata kunci, klasterisasi sumber |
| `references/synthesis-contract.md` | 6 LAWs disiplin kutipan saat menulis ulang hasil riset |
| `references/content-rules.md` | Aturan konten: ringkasan, heading, provenance klaim |
| `references/geo-optimization.md` | Optimasi kesiapan dikutip AI |
| `references/ai-crawler-guide.md` | Panduan crawler AI per vendor |
| `references/google-landscape-2026.md` | Lanskap fitur pencarian Google 2026 beserta sumber |
| `references/video-embeds.md` | Kriteria pemilihan dan penandaan video (untuk usulan ke operator) |
| `references/schema-stack.md` | Detail tumpukan schema (untuk halaman non-artikel) |
| `references/flow-alignment.md` | Pemetaan disiplin bukti FLOW (adaptasi) |
