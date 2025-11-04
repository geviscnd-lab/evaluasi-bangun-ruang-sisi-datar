import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Evaluasi Bangun Ruang Sisi Datar", layout="wide")

# Judul Aplikasi
st.title("🧮 Evaluasi Bangun Ruang Sisi Datar")
st.write("Aplikasi ini berisi 10 soal pilihan ganda untuk mengukur kemampuan berpikir kritis siswa dalam menyelesaikan masalah kehidupan sehari-hari yang berkaitan dengan bangun ruang sisi datar.")

# Pilihan peran
role = st.radio("Pilih peran Anda:", ["Siswa", "Guru"])

# Data soal
QUESTIONS = [
    {
        "no": 1,
        "soal": "Sebuah kotak berbentuk balok dengan ukuran 60 cm × 40 cm × 30 cm akan dicat seluruh permukaannya. Berapa luas permukaannya?",
        "options": ["7800 cm²", "11400 cm²", "13200 cm²", "15600 cm²"],
        "answer": "11400 cm²"
    },
    {
        "no": 2,
        "soal": "Sebuah prisma segitiga memiliki alas dengan luas 12 cm² dan tinggi 10 cm. Berapa volumenya?",
        "options": ["120 cm³", "240 cm³", "60 cm³", "12 cm³"],
        "answer": "120 cm³"
    },
    {
        "no": 3,
        "soal": "Seorang tukang membuat tong sampah berbentuk tabung dengan tutup kerucut. Jika volume total harus < 50.000 cm³, ukuran yang paling tepat adalah...",
        "options": [
            "Volume tabung 45.000 cm³ + kerucut 4.000 cm³",
            "Volume tabung 30.000 cm³ + kerucut 20.000 cm³",
            "Volume tabung 60.000 cm³",
            "Volume tabung 49.999 cm³ + kerucut 2 cm³"
        ],
        "answer": "Volume tabung 45.000 cm³ + kerucut 4.000 cm³"
    },
    {
        "no": 4,
        "soal": "Sebuah limas alas persegi sisi 8 cm dan tinggi 9 cm. Berapa volumenya?",
        "options": ["192 cm³", "384 cm³", "1536 cm³", "576 cm³"],
        "answer": "192 cm³"
    },
    {
        "no": 5,
        "soal": "Mengapa penting mempertimbangkan sambungan/overlap saat merakit kotak dari karton?",
        "options": [
            "Agar terlihat rapi saja",
            "Agar muatan tidak keluar dan sambungan kuat",
            "Agar menghemat cat",
            "Tidak berpengaruh"
        ],
        "answer": "Agar muatan tidak keluar dan sambungan kuat"
    },
    {
        "no": 6,
        "soal": "Sebuah kubus rusuk 5 cm dibungkus kertas kado. Luas kertas minimal yang dibutuhkan adalah...",
        "options": ["150 cm²", "300 cm²", "1500 cm²", "750 cm²"],
        "answer": "1500 cm²"
    },
    {
        "no": 7,
        "soal": "Pertimbangan kritis memilih atap prisma segitiga vs limas segiempat adalah...",
        "options": [
            "Estetika semata",
            "Volume, kemudahan konstruksi, dan aliran air",
            "Hanya biaya material",
            "Warna cat"
        ],
        "answer": "Volume, kemudahan konstruksi, dan aliran air"
    },
    {
        "no": 8,
        "soal": "Sebuah kerucut es krim tinggi 12 cm dan jari-jari 3 cm. Volumenya adalah...",
        "options": ["36π cm³", "12π cm³", "36π/3 cm³", "9π cm³"],
        "answer": "36π cm³"
    },
    {
        "no": 9,
        "soal": "Saat memindahkan barang berbentuk balok ke mobil, pendekatan terbaik adalah...",
        "options": [
            "Langsung angkat",
            "Mengukur dimensi dan menyusun stabil",
            "Masukkan tanpa rencana",
            "Tebak saja muat"
        ],
        "answer": "Mengukur dimensi dan menyusun stabil"
    },
    {
        "no": 10,
        "soal": "Prisma segiempat beraturan alas sisi 7 cm dan tinggi 10 cm. Luas permukaan totalnya adalah...",
        "options": ["686 cm²", "392 cm²", "266 cm²", "420 cm²"],
        "answer": "420 cm²"
    }
]

if role == "Siswa":
    nama = st.text_input("Nama Siswa:")
    kelas = st.text_input("Kelas:")

    st.markdown("---")
    st.header("📘 Soal Evaluasi")

    answers = []
    reasons = []

    for q in QUESTIONS:
        st.subheader(f"Soal {q['no']}")
        st.write(q["soal"])
        answer = st.radio("Pilih jawaban:", q["options"], key=f"ans_{q['no']}")
        reason = st.text_area("Tulis alasan (1–2 kalimat):", key=f"reason_{q['no']}")
        answers.append(answer)
        reasons.append(reason)
        st.markdown("---")

    if st.button("Kirim dan Unduh Hasil (Excel)"):
        correct = sum(1 for i, q in enumerate(QUESTIONS) if answers[i] == q["answer"])
        score = f"{correct} / {len(QUESTIONS)}"

        df = pd.DataFrame({
            "No": [q["no"] for q in QUESTIONS],
            "Soal": [q["soal"] for q in QUESTIONS],
            "Jawaban Siswa": answers,
            "Jawaban Benar": [q["answer"] for q in QUESTIONS],
            "Benar?": ["YA" if answers[i] == q["answer"] else "TIDAK" for i, q in enumerate(QUESTIONS)],
            "Alasan": reasons
        })

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"hasil_{nama}_{now}.xlsx"
        df.to_excel(filename, index=False)

        st.success(f"Skor kamu: {score}")
        st.download_button("💾 Download Hasil Excel", data=open(filename, "rb"), file_name=filename)

elif role == "Guru":
    st.header("👩‍🏫 Panduan Guru")
    st.write("""
    1. Bagikan aplikasi ini ke siswa (bisa di-host lewat Codespaces atau Streamlit Cloud).
    2. Siswa akan mengisi nama, kelas, dan mengerjakan soal.
    3. Setelah selesai, mereka akan mendapatkan file **Excel** hasil pekerjaan.
    4. Guru dapat mengumpulkan file Excel tersebut untuk penilaian.
    
    ### Rubrik Penilaian:
    - **Ketepatan jawaban**: 1 poin per benar  
    - **Kedalaman alasan**: 0–2 poin  
    - **Relevansi alasan**: 0–2 poin  
    Total per soal maksimal **5 poin**.
    """)
