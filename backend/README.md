# Market Intelligence

Repositori ini berisi pipeline otomatis untuk menghasilkan ringkasan intelijen perusahaan (company brief) berdasarkan data publik, sumber web, analisis finansial, serta deteksi kemampuan dan kebutuhan teknologi.

## Ringkasan Proyek

Proyek ini dirancang untuk membantu pengguna mengidentifikasi informasi perusahaan secara terstruktur, mulai dari:

- resolusi perusahaan dan pencarian sumber resmi,
- crawling halaman web dan ekstraksi konten penting,
- ekstraksi fakta dari dokumen/halaman menggunakan model AI,
- analisis finansial dari data IDX,
- deteksi capability dan teknologi yang relevan,
- pembuatan laporan singkat dalam format Markdown.

Tujuan utamanya adalah menghasilkan brief perusahaan yang dapat dipakai untuk riset pasar, analisis kompetitor, atau persiapan meeting bisnis.

## Fitur Utama

- Pencarian sumber perusahaan melalui Tavily
- Crawling halaman website dengan Crawl4AI
- Seleksi tautan penting dan penggabungan konten multi-halaman
- Pembersihan markdown untuk data yang lebih rapi
- Ekstraksi fakta perusahaan menggunakan Gemini
- Integrasi data finansial dari IDX
- Deteksi business capabilities dan technology needs
- Pembuatan report Markdown otomatis

## Arsitektur / Alur Kerja

Alur kerja utama proyek ini mengikuti proses berikut:

1. Input nama perusahaan dari pengguna
2. Resolusi perusahaan dan pencarian website resmi
3. Crawling halaman perusahaan
4. Ekstraksi tautan penting
5. Pembersihan dan penggabungan konten
6. Ekstraksi fakta perusahaan dengan AI
7. Pengayaan data finansial dan analisis bisnis
8. Pembuatan laporan final dalam format Markdown

Untuk gambaran lebih rinci, lihat dokumen di folder docs:

- docs/flow.md
- docs/report_structure.md
- docs/company_schema.md

## Struktur Folder

- main.py — entry point interaktif untuk menjalankan pipeline
- src/pipeline/pipeline.py — inti alur kerja utama
- src/source_discovery/ — pencarian sumber perusahaan
- src/crawler/ — crawling dan pemrosesan website
- src/fact_extraction/ — ekstraksi fakta dari konten
- src/financial_intelligence/ — pengambilan data finansial IDX
- src/capability_detection/ — deteksi kapabilitas bisnis
- src/technology_needs/ — deteksi kebutuhan teknologi
- src/report_generator/ — pembuatan report
- docs/ — dokumentasi alur dan struktur output

## Persyaratan

- Python 3.12
- Dependensi yang tercantum di pyproject.toml dan requirements.txt
- Kunci API:
  - GOOGLE_API_KEY
  - TAVILY_API_KEY

## Instalasi

### Dengan uv

```bash
uv sync
```

### Dengan pip

```bash
pip install -r requirements.txt
```

## Konfigurasi Environment

Buat file environment untuk API key yang dibutuhkan. File ini dipakai oleh pipeline saat menjalankan proses.

Contoh variabel yang digunakan:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Menjalankan Aplikasi

Jalankan program interaktif berikut:

```bash
uv run main.py
```

Atau jika menggunakan Python biasa:

```bash
python main.py
```

Saat dijalankan, program akan meminta nama perusahaan lalu menghasilkan file output seperti:

- nama_perusahaan_cleaned.md
- nama_perusahaan_brief.md

## Output yang Dihasilkan

- file markdown hasil pembersihan konten website
- file brief perusahaan yang berisi ringkasan, analisis, kapabilitas, dan kebutuhan teknologi

## Catatan Penggunaan

- Proyek ini sangat bergantung pada API eksternal (Google AI dan Tavily).
- Hasil kualitas sangat dipengaruhi oleh ketersediaan data publik dan keakuratan sumber yang ditemukan.
- Untuk pengembangan lebih lanjut, Anda dapat memperluas modul di folder src sesuai kebutuhan pipeline.

## Lisensi

Proyek ini menggunakan lisensi MIT sesuai definisi di pyproject.toml.
