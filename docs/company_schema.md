# Skema Data Perusahaan

Dokumen ini menjelaskan field utama yang dipakai dalam proses ekstraksi fakta perusahaan oleh pipeline.

## Company Profile

- company_name: nama perusahaan
- industry: daftar industri atau kategori bisnis
- description: deskripsi singkat perusahaan
- headquarters: alamat atau kantor pusat
- products_services: daftar produk dan layanan
- subsidiaries: daftar anak perusahaan atau unit bisnis terkait
- partnerships: daftar kemitraan atau kolaborasi
- available_documents: dokumen atau laporan yang disebutkan
- investor_relations: status hubungan investor

## Financial Information

- ticker: kode saham (jika ada)
- sector: sektor industri utama
- sub_sector: sub-sektor
- listing_board: papan pencatatan di bursa
- latest_financial_period: periode laporan keuangan terbaru
- revenue: pendapatan
- net_income: laba bersih
- total_assets: total aset
- total_liabilities: total kewajiban
- total_equity: total ekuitas

## Analysis Output

- business_capabilities: daftar kapabilitas bisnis yang terdeteksi
- technology_needs: daftar kebutuhan teknologi yang teridentifikasi

## Catatan Implementasi

Struktur field ini mengacu pada model CompanyFacts yang didefinisikan di src/fact_extraction/models.py, serta data finansial yang diproses di src/financial_intelligence/models.py.