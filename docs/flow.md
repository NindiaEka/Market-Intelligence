# Alur Pipeline Market Intelligence

Dokumen ini menjelaskan alur kerja yang saat ini digunakan oleh proyek.

1. Input nama perusahaan dari pengguna
2. Pencarian data finansial dan profil perusahaan (jika tersedia melalui IDX)
3. Jika data IDX tidak tersedia, pencarian sumber resmi melalui Tavily
4. Crawling halaman website perusahaan
5. Ekstraksi tautan penting dari halaman yang ditemukan
6. Crawling halaman penting secara multi-page
7. Pembersihan konten Markdown hasil crawling
8. Ekstraksi fakta perusahaan menggunakan model AI
9. Pengayaan data finansial, sektor, dan informasi perusahaan
10. Deteksi business capabilities dan technology needs
11. Pembuatan laporan ringkas dalam format Markdown

## Diagram Alur

User Input
↓
Financial Intelligence / Company Resolution
↓
Source Discovery (jika diperlukan)
↓
Web Crawling
↓
Link Extraction
↓
Multi-page Crawling
↓
Markdown Cleaning
↓
Fact Extraction (Gemini)
↓
Capability + Technology Detection
↓
Company Brief Report

## Output yang Dihasilkan

- file hasil pembersihan konten website: nama_perusahaan_cleaned.md
- file brief perusahaan: nama_perusahaan_brief.md