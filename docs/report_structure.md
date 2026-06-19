# Struktur Laporan Market Intelligence

Laporan yang dihasilkan oleh pipeline saat ini mengikuti format ringkas yang tersusun dari fakta perusahaan, data finansial, serta analisis kapabilitas dan teknologi.

## 1. Header Perusahaan

Bagian awal berisi nama perusahaan utama.

## 2. Overview

Ringkasan singkat mengenai deskripsi perusahaan dan konteks bisnisnya.

## 3. Financial Information

Bagian ini menampilkan data finansial yang relevan, antara lain:

- Ticker
- Sector
- Sub Sector
- Listing Board
- Latest Financial Report
- Revenue
- Net Income
- Total Assets
- Total Liabilities
- Total Equity

## 4. Industry

Informasi sektor industri perusahaan yang didapat dari data IDX atau hasil ekstraksi.

## 5. Headquarters

Alamat atau lokasi kantor pusat perusahaan.

## 6. Products & Services

Daftar produk, layanan, atau solusi yang ditawarkan perusahaan.

## 7. Business Capabilities

Analisis kapabilitas bisnis yang terdeteksi dari konten perusahaan, misalnya:

- layanan digital,
- kemampuan operasi,
- kompetensi teknologi,
- aspek bisnis strategis.

## 8. Potential Technology Needs

Daftar kebutuhan teknologi yang potensial berdasarkan profil perusahaan dan analisis konten.

## 9. Partnerships

Informasi mitra, kolaborasi, atau kerja sama yang ditemukan dalam sumber publik.

## 10. Investor Relations

Status atau catatan terkait hubungan investor yang teridentifikasi.

## Catatan

Struktur ini disusun agar selaras dengan template yang digunakan di src/report_generator/templates.py dan data yang dihasilkan oleh src/fact_extraction/models.py.