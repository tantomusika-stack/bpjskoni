# Generator Surat Keterangan KONI — Template Asli

Aplikasi Streamlit untuk mengisi Nama, NIK, dan Cabor pada PDF template asli. Template disertakan sebagai `template_surat.pdf`, sehingga kop, tata letak, serta elemen tanda tangan/stempel yang memang sudah ada di PDF sumber tetap dipertahankan.

## File
- `app.py` — aplikasi.
- `template_surat.pdf` — PDF template asli.
- `requirements.txt` — dependensi.

## Deploy
1. Buat repository GitHub baru.
2. Upload ketiga file di atas ke direktori utama repository.
3. Buka https://share.streamlit.io/ dan masuk dengan GitHub.
4. Buat aplikasi dari repository, pilih `app.py` sebagai Main file path, lalu deploy.

## Catatan
- Aplikasi hanya mengisi Nama, NIK, dan Cabor. Nomor/tanggal surat serta isi lain tetap seperti template.
- Validasi NIK: 16 digit.
- Setelah deploy, uji hasil PDF dan periksa posisi teks sebelum digunakan resmi.
