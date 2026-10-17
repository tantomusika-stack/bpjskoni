import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO
import re
from pathlib import Path

st.set_page_config(page_title="Surat Keterangan KONI", page_icon="📄", layout="centered")
st.title("📄 Generator Surat Keterangan KONI")
st.caption("KONI Kabupaten Tangerang")
st.write("Isi Nama, NIK, dan Cabor. Aplikasi akan menempatkan data pada template PDF asli agar kop surat, tanda tangan, stempel, dan tata letak yang sudah ada tetap dipertahankan.")

TEMPLATE_PATH = Path(__file__).parent / "template_surat.pdf"

with st.form("form_atlet"):
    nama = st.text_input("Nama lengkap", placeholder="Sesuai identitas")
    nik = st.text_input("NIK", max_chars=16, placeholder="16 digit angka")
    cabor = st.text_input("Cabang olahraga (Cabor)", placeholder="Contoh: Pencak Silat")
    submit = st.form_submit_button("Buat PDF", type="primary", use_container_width=True)

def fit_font_size(text, max_width, start=11, min_size=7):
    size = start
    while size > min_size and fitz.get_text_length(text, fontname="helv", fontsize=size) > max_width:
        size -= 0.25
    return size

def create_pdf(nama, nik, cabor):
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError("File template_surat.pdf tidak ditemukan. Pastikan file ini ada bersama app.py.")
    doc = fitz.open(TEMPLATE_PATH)
    page = doc[0]

    # Posisi di bawah menggunakan koordinat halaman template asli (A4).
    # Hanya area titik-titik Nama, NIK, dan Cabor yang ditutup lalu diisi.
    entries = [
        (nama, fitz.Rect(158, 299, 525, 316), (162, 312)),
        (nik,  fitz.Rect(158, 314, 525, 331), (162, 326.6)),
        (cabor,fitz.Rect(158, 328.6, 525, 345.6), (162, 341.2)),
    ]
    for value, rect, point in entries:
        page.draw_rect(rect, color=None, fill=(1, 1, 1), overlay=True)
        fontsize = fit_font_size(value, rect.width - 8)
        page.insert_text(point, value, fontname="helv", fontsize=fontsize,
                         color=(0, 0, 0), overlay=True)

    output = BytesIO(doc.tobytes(garbage=4, deflate=True))
    doc.close()
    output.seek(0)
    return output.getvalue()

if submit:
    nama = nama.strip()
    nik = nik.strip()
    cabor = cabor.strip()
    if not nama or not nik or not cabor:
        st.error("Mohon isi Nama, NIK, dan Cabor.")
    elif not re.fullmatch(r"\d{16}", nik):
        st.error("NIK harus terdiri dari 16 digit angka.")
    else:
        try:
            pdf_bytes = create_pdf(nama, nik, cabor)
            safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", nama).strip("_") or "Atlet"
            st.success("PDF berhasil dibuat menggunakan template asli.")
            st.download_button(
                "⬇️ Download Surat Keterangan PDF",
                data=pdf_bytes,
                file_name=f"Surat_Keterangan_KONI_{safe_name}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Gagal membuat PDF: {e}")

st.caption("Catatan: template asli dipakai sebagai dasar, sehingga elemen desain yang sudah ada tetap ada. Periksa posisi hasil PDF sebelum digunakan.")
