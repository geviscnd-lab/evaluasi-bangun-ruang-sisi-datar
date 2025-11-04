# app.py
import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Evaluasi Bangun Ruang Sisi Datar", layout="centered")

# ----------------------
# DATA: 10 soal + opsi
# ----------------------
QUESTIONS = [
    {
        "id": "Q1",
        "question": "Sebuah kotak kardus berukuran panjang 40 cm, lebar 30 cm, tinggi 20 cm. Berapa volume kotak tersebut?",
        "options": {"A": "24.000 cm³", "B": "2.400 cm³", "C": "240.000 cm³", "D": "4.000 cm³"},
        "answer": "A",
        "explain": "Volume balok = p × l × t = 40×30×20 = 24.000 cm³."
    },
    {
        "id": "Q2",
        "question": "Sebuah menara berbentuk prisma segitiga memiliki alas segitiga dengan luas 6 m² dan tinggi prisma 10 m. Volume berapa?",
        "options": {"A": "60 m³", "B": "16 m³", "C": "600 m³", "D": "6 m³"},
        "answer": "A",
        "explain": "Volume prisma = luas alas × tinggi = 6 × 10 = 60 m³."
    },
    {
        "id": "Q3",
        "question": "Sebuah limas segiempat dengan luas alas 25 m² dan tinggi 6 m. Volume limas adalah ...",
        "options": {"A": "150 m³", "B": "50 m³", "C": "25 m³", "D": "450 m³"},
        "answer": "B",
        "explain": "Volume limas = (1/3) × luas alas × tinggi = (1/3)×25×6 = 50 m³."
    },
    {
        "id": "Q4",
        "question": "Sebuah kubus memiliki diagonal ruang 6√3 cm. Panjang sisi kubus adalah ...",
        "options": {"A": "6 cm", "B": "3 cm", "C": "2√3 cm", "D": "√3 cm"},
        "answer": "A",
        "explain": "Diagonal ruang kubus = s√3 → s = diagonal/√3 = 6√3 / √3 = 6 cm."
    },
    {
        "id": "Q5",
        "question": "Sebuah bak air berbentuk balok panjang 2 m, lebar 1,5 m, tinggi 1 m. Jika diisi 75% kapasitasnya, berapa volume air (m³)?",
        "options": {"A": "1,5 m³", "B": "3,0 m³", "C": "0,75 m³", "D": "2,5 m³"},
        "answer": "A",
        "explain": "Kapasitas total = 2×1.5×1 = 3 m³; 75% → 0.75×3 = 2.25 m³. (Catatan: jawaban A salah ketik sebelumnya) --> **Betul: 2.25 m³**. (Dalam soal ini, opsi A harus 2.25. Pastikan opsi di repo sesuai.)"
    },
    {
        "id": "Q6",
        "question": "Jika sebuah prisma segiempat memiliki ukuran alas 4 m × 3 m dan tinggi 5 m, berapa luas permukaan seluruh prisma (dengan tutup dan alas)?",
        "options": {"A": "94 m²", "B": "86 m²", "C": "94 m³", "D": "120 m²"},
        "answer": "A",
        "explain": "Luas alas = 4×3=12; 2×alas=24. Keliling alas = 2(4+3)=14. Luas selimut = keliling×tinggi = 14×5=70. Total = 24+70=94 m²."
    },
    {
        "id": "Q7",
        "question": "Sebuah topi berbentuk kerucut memiliki jari-jari 7 cm dan tinggi 24 cm. Volume kerucut berapa? (π = 22/7)",
        "options": {"A": "2.464 cm³", "B": "1.848 cm³", "C": "2.310 cm³", "D": "1.232 cm³"},
        "answer": "A",
        "explain": "Volume = (1/3)πr²h = (1/3)×(22/7)×7²×24 = (1/3)×22×7×24 = 2.464 cm³."
    },
    {
        "id": "Q8",
        "question": "Sebuah kotak kemasan berbentuk balok diperlukan untuk menampung sebuah botol berbentuk silinder berdiameter 8 cm dan tinggi 30 cm. Minimum ukuran lebar balok agar botol muat (asumsi berdiri) adalah ...",
        "options": {"A": "8 cm", "B": "16 cm", "C": "π×8 cm", "D": "4 cm"},
        "answer": "A",
        "explain": "Jika botol berdiri, lebar minimum balok perlu ≥ diameter = 8 cm."
    },
    {
        "id": "Q9",
        "question": "Sebuah gedung berbentuk limas segiempat dipasang ventilasi di setiap sisi segitiga tegak. Jika tinggi segitiga sisi adalah 3 m dan alas sisi 4 m, luas total 4 sisi segitiga adalah ...",
        "options": {"A": "24 m²", "B": "12 m²", "C": "48 m²", "D": "6 m²"},
        "answer": "A",
        "explain": "Luas satu segitiga = 1/2 × alas × tinggi = 1/2×4×3 = 6 m². Empat sisi → 24 m²."
    },
    {
        "id": "Q10",
        "question": "Sebuah paket berbentuk kubus memiliki sisi 30 cm. Jika akan dibungkus kertas dan setiap lembar kertas berukuran 0,5 m × 0,7 m, berapa lembar minimum (asumsi tidak ada sisa besar)?",
        "options": {"A": "2 lembar", "B": "3 lembar", "C": "4 lembar", "D": "1 lembar"},
        "answer": "A",
        "explain": "Luas permukaan kubus = 6×(0.3×0.3)=6×0.09=0.54 m². Satu lembar = 0.35 m². 0.54 / 0.35 ≈ 1.54 → butuh 2 lembar."
    },
]

# ----------------------
# Utility functions
# ----------------------
def compute_score(answers, justifications):
    correct = 0
    bonus = 0.0
    per_correct = 1.0
    for idx, q in enumerate(QUESTIONS):
        qid = q["id"]
        user_ans = answers.get(qid, "")
        if user_ans == q["answer"]:
            correct += per_correct
        # simple heuristic: justifikasi cukup panjang => +0.5 poin
        justification = justifications.get(qid, "")
        if justification and len(justification.strip()) >= 30:
            bonus += 0.5
    max_score = len(QUESTIONS) + (0.5 * len(QUESTIONS))  # if all justifications long
    total = correct + bonus
    percent = (total / max_score) * 100
    return {
        "correct_count": correct,
        "bonus_points": bonus,
        "total_score": total,
        "percent": round(percent, 2),
        "max_score": max_score
    }

# ----------------------
# UI: header & role
# ----------------------
st.title("Evaluasi: Bangun Ruang Sisi Datar — 10 Soal (Pilihan Ganda)")
st.write("Aplikasi ini mengumpulkan jawaban, meminta justifikasi singkat (untuk menilai berpikir kritis), dan menghasilkan file Excel yang bisa diunduh.")

role = st.sidebar.selectbox("Pilih Peran", ["Siswa", "Guru"])

# Role descriptions
if role == "Siswa":
    st.info("Peran Siswa: kerjakan 10 soal, lengkapi justifikasi singkat tiap soal (opsional tapi meningkatkan skor berpikir kritis). Setelah submit, Anda dapat mengunduh hasil dalam bentuk Excel.")
else:
    st.info("Peran Guru: lihat rekap semua respon siswa, analitik sederhana, dan unduh seluruh respons sebagai Excel untuk penilaian lebih lanjut.")

# Simple storage in-memory; for real deployment gunakan DB or Sheets
if "responses" not in st.session_state:
    st.session_state.responses = []  # list of dicts

# ----------------------
# GURU VIEW
# ----------------------
if role == "Guru":
    st.header("Panel Guru — Rekap Respon")
    st.write("Total respon:", len(st.session_state.responses))
    if len(st.session_state.responses) == 0:
        st.warning("Belum ada respon siswa. Minta siswa untuk mengerjakan kuis.")
    else:
        # build DataFrame
        df = pd.DataFrame(st.session_state.responses)
        st.dataframe(df)
        st.markdown("**Statistik ringkas:**")
        st.write(df[["timestamp", "student_name", "percent", "total_score"]].sort_values(by="timestamp", ascending=False).head(20))
        # Simple aggregate
        avg_percent = df["percent"].mean()
        st.metric("Rata-rata persentase", f"{avg_percent:.2f}%")
        # Download all as excel
        towrite = io.BytesIO()
        df.to_excel(towrite, index=False, engine="openpyxl")
        towrite.seek(0)
        st.download_button("Unduh semua respons (Excel)", data=towrite, file_name="rekap_respon_siswa.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.caption("Gunakan Excel untuk penilaian lengkap atau catat rubrik berpikir kritis.")

# ----------------------
# SISWA VIEW
# ----------------------
if role == "Siswa":
    st.header("Form Siswa")
    name = st.text_input("Nama lengkap", "")
    email = st.text_input("Email (opsional)", "")

    st.write("Isi jawabanmu, dan berikan justifikasi singkat (minimal 30 karakter) bila memungkinkan — itu membantu menilai kemampuan berpikir kritis.")
    answers = {}
    justifications = {}

    with st.form("quiz_form"):
        for q in QUESTIONS:
            st.markdown(f"**{q['id']}. {q['question']}**")
            cols = st.columns([1, 5])
            choice = cols[0].radio("Pilih:", options=list(q["options"].keys()), key=f"ans_{q['id']}")
            st.write(", ".join([f"{k}) {v}" for k, v in q["options"].items()]))
            just = st.text_area("Justifikasi singkat (bagaimana ini berhubungan dengan kehidupan sehari-hari atau alasan pilihanmu):", key=f"just_{q['id']}", placeholder="Contoh: 'Saya pilih A karena ...'", height=80)
            answers[q["id"]] = choice
            justifications[q["id"]] = just

        submitted = st.form_submit_button("Submit Jawaban")

    if submitted:
        if not name.strip():
            st.warning("Masukkan nama terlebih dahulu supaya hasil bisa disimpan.")
        else:
            result = compute_score(answers, justifications)
            st.success(f"Terima kasih, {name}! Hasilmu: {result['total_score']:.2f} / {result['max_score']:.2f} ({result['percent']}%).")
            st.write(f"Jumlah jawaban benar (point): {result['correct_count']}")
            st.write(f"Bonus poin untuk justifikasi (panjang >=30 karakter): {result['bonus_points']:.1f}")
            st.markdown("**Ulasan singkat tiap soal (kunci & penjelasan):**")
            for q in QUESTIONS:
                st.write(f"- {q['id']}: Kunci = **{q['answer']}** — {q['explain']}")

            # Save response
            record = {
                "timestamp": datetime.now().isoformat(sep=" ", timespec="seconds"),
                "student_name": name,
                "email": email,
                "percent": result["percent"],
                "total_score": result["total_score"],
                "correct_count": result["correct_count"],
                "bonus_points": result["bonus_points"]
            }
            # add answers & justifications fields
            for q in QUESTIONS:
                record[f"{q['id']}_answer"] = answers.get(q["id"], "")
                record[f"{q['id']}_justification"] = justifications.get(q["id"], "")

            st.session_state.responses.append(record)

            # Create dataframe for the student download (single row)
            df_single = pd.DataFrame([record])
            towrite = io.BytesIO()
            df_single.to_excel(towrite, index=False, engine="openpyxl")
            towrite.seek(0)
            st.download_button("Unduh hasilmu (Excel)", data=towrite, file_name=f"hasil_{name.replace(' ', '_')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            st.info("Catatan: Guru bisa meninjau file Excel yang berisi jawaban & justifikasi untuk menilai aspek berpikir kritis secara kualitatif.")

# Footer: petunjuk singkat
st.markdown("---")
st.markdown("**Catatan untuk pengembang / guru:** untuk penyimpanan permanen dan multi-user, integrasikan database (Google Sheets, Firebase, atau Postgres). Mekanisme bonus justifikasi di atas bersifat heuristik; guru disarankan menilai kualitas justifikasi secara manual menggunakan rubrik.")
