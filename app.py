# Repository: evaluasi-bangun-ruang-sisi-datar

This single-file preview contains a ready-to-run React app (single-file component + README + package.json) that implements:

- A 10-question multiple-choice quiz about "bangun ruang sisi datar" (polyhedral solids with flat faces) focused on measuring critical thinking in everyday application problems.
- Student and Teacher roles (selectable). Students take the quiz and give short reasoning for each answer. After submission the app calculates scores and creates an Excel (.xlsx) file containing the student's answers, reasoning, score, and timestamp which can be downloaded directly.
- Teacher role shows an example template and instructions for collecting student files and evaluating them.

---

## Files included (in this single preview):

### package.json

```json
{
  "name": "evaluasi-bangun-ruang-sisi-datar",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "xlsx": "^0.18.5"
  },
  "scripts": {
    "start": "vite",
    "build": "vite build"
  }
}
```

(You can also set this up with Create React App; the code is framework-agnostic — it uses standard React imports and the `xlsx` library to generate Excel files.)

---

### README.md (short)

```
Repository name: evaluasi-bangun-ruang-sisi-datar
Description: A small React web app that presents 10 multiple-choice questions about polyhedral solids (bangun ruang sisi datar) designed to measure students' critical thinking for real-life problem solving. Students submit answers + short reasoning; the app produces a downloadable Excel report per attempt.

How to run:
1. git clone <repo-url>
2. npm install
3. npm start

What the teacher should do:
- Share the app URL with students or host it on GitHub Pages / Netlify / Vercel.
- Ask students to enter their name/class when taking the quiz so exported Excel files can be tracked.
- Collect the Excel files and grade the reasoning columns manually or import to a gradebook.

What the student should do:
- Choose role "Student", fill name/class, answer each multiple choice and add 1-2 sentence reasoning for each answer.
- Submit and download the Excel report, then upload to the teacher's LMS or send by email.
```

---

### src/App.jsx

```jsx
import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import * as XLSX from 'xlsx';

const QUESTIONS = [
  {
    id: 1,
    text: 'Sebuah kotak berbentuk balok dimensi 60 cm x 40 cm x 30 cm. Jika ingin mengecat bagian luar kotak (seluruh permukaan luar), berapa luas permukaan yang harus dicat? (Pertimbangkan pemikiran langkah-langkah dan pilih jawaban yang benar)',
    choices: [
      '7800 cm²',
      '11400 cm²',
      '13200 cm²',
      '15600 cm²'
    ],
    answer: 2 // 11400
  },
  {
    id: 2,
    text: 'Sebuah prisma segitiga memiliki alas segitiga dengan luas 12 cm² dan tinggi prisma 10 cm. Volume prisma tersebut adalah…',
    choices: ['120 cm³', '240 cm³', '60 cm³', '12 cm³'],
    answer: 0
  },
  {
    id: 3,
    text: 'Seorang tukang ingin membuat tong sampah bentuk tabung dengan tutup berbentuk kerucut. Jika volume total harus kurang dari 50.000 cm³, pendekatan mana yang paling tepat untuk memilih ukuran? (pilih jawaban numerik yang benar)',
    choices: ['Volume tabung 45.000 cm³ + kerucut 4.000 cm³', 'Volume tabung 30.000 cm³ + kerucut 20.000 cm³', 'Volume tabung 60.000 cm³', 'Volume tabung 49.999 cm³ + kerucut 2 cm³'],
    answer: 0
  },
  {
    id: 4,
    text: 'Sebuah limas segiempat alasnya berbentuk persegi 8 cm sisi. Tinggi limas 9 cm. Berapa volume limas?',
    choices: ['192 cm³', '384 cm³', '1536 cm³', '576 cm³'],
    answer: 0
  },
  {
    id: 5,
    text: 'Mengapa penting mempertimbangkan jaringan sambungan / overlap saat merakit kotak dari karton untuk mengemas barang? (pilih jawaban yang paling terkait pemikiran kritis)',
    choices: [
      'Agar terlihat rapi saja',
      'Agar muatan tidak keluar dan kekuatan sambungan cukup pada titik beban',
      'Agar menghemat cat',
      'Tidak berpengaruh pada kekuatan kemasan'
    ],
    answer: 1
  },
  {
    id: 6,
    text: 'Sebuah bangun ruang sisi datar—kubus—memiliki rusuk 5 cm. Jika ingin membungkusnya dengan kertas kado dengan sisa minimal, luas kertas minimum yang diperlukan kira-kira…',
    choices: ['150 cm²', '300 cm²', '1500 cm²', '750 cm²'],
    answer: 2
  },
  {
    id: 7,
    text: 'Seorang arsitek mempertimbangkan bentuk atap berupa prisma segitiga vs limas segiempat untuk ruang penyimpanan. Pertimbangan pemikiran kritis apa yang paling relevan?',
    choices: ['Estetika semata', 'Volume dan kemudahan konstruksi serta pengaliran air', 'Hanya biaya material', 'Warna cat'],
    answer: 1
  },
  {
    id: 8,
    text: 'Sebuah kerucut es krim memiliki tinggi 12 cm dan jari-jari 3 cm. Volume es krim (kerucut) adalah…',
    choices: ['36π cm³', '36π/3 cm³', '36π/9 cm³', '12π cm³'],
    answer: 1
  },
  {
    id: 9,
    text: 'Jika kita ingin memindahkan beberapa barang berbentuk balok ke mobil, apa pendekatan kritis terbaik sebelum mengangkat?',
    choices: ['Mengira muatan muat saja', 'Mengukur dimensi dan susunan sehingga muatan stabil dan aman', 'Angkat secepat mungkin', 'Masukkan tanpa perencanaan'],
    answer: 1
  },
  {
    id: 10,
    text: 'Sebuah prisma segiempat beraturan memiliki alas persegi 7 cm sisi dan tinggi 10 cm. Luas permukaan total (termuat semua sisi) adalah…',
    choices: ['686 cm²', '392 cm²', '266 cm²', '420 cm²'],
    answer: 3
  }
];

function formatTimestamp() {
  return new Date().toLocaleString();
}

function App() {
  const [role, setRole] = useState('student');
  const [name, setName] = useState('');
  const [kelas, setKelas] = useState('');
  const [answers, setAnswers] = useState(() => QUESTIONS.map(() => ({ choice: null, reason: '' })));
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(null);

  function handleChoice(qIdx, choiceIdx) {
    const copy = [...answers];
    copy[qIdx] = { ...copy[qIdx], choice: choiceIdx };
    setAnswers(copy);
  }
  function handleReason(qIdx, text) {
    const copy = [...answers];
    copy[qIdx] = { ...copy[qIdx], reason: text };
    setAnswers(copy);
  }

  function computeScore() {
    let s = 0;
    QUESTIONS.forEach((q, i) => {
      if (answers[i].choice === q.answer) s += 1;
    });
    return s;
  }

  function handleSubmit() {
    const s = computeScore();
    setScore(s);
    setSubmitted(true);
    // create excel
    const rows = QUESTIONS.map((q, i) => ({
      'No': q.id,
      'Pertanyaan': q.text,
      'Pilihan Pilihan (0-based index)': answers[i].choice,
      'Isi Pilihan': answers[i].choice != null ? q.choices[answers[i].choice] : '',
      'Jawaban Benar': q.choices[q.answer],
      'Alasan Siswa': answers[i].reason,
      'Benar?': answers[i].choice === q.answer ? 'YA' : 'TIDAK'
    }));

    const meta = {
      'Nama Siswa': name,
      'Kelas': kelas,
      'Skor': `${s} / ${QUESTIONS.length}`,
      'Waktu': formatTimestamp()
    };

    const wsData = [
      ['Nama Siswa', meta['Nama Siswa']],
      ['Kelas', meta['Kelas']],
      ['Skor', meta['Skor']],
      ['Waktu', meta['Waktu']],
      [],
      ['No', 'Pertanyaan', 'Pilihan Index', 'Isi Pilihan', 'Jawaban Benar', 'Alasan Siswa', 'Benar?']
    ];

    rows.forEach(r => {
      wsData.push([r['No'], r['Pertanyaan'], r['Pilihan Pilihan (0-based index)'], r['Isi Pilihan'], r['Jawaban Benar'], r['Alasan Siswa'], r['Benar?']]);
    });

    const ws = XLSX.utils.aoa_to_sheet(wsData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Hasil');

    const filename = `${name || 'siswa'}_${(new Date()).toISOString().slice(0,19).replace(/[:T]/g,'-')}_hasil.xlsx`;
    XLSX.writeFile(wb, filename);
  }

  return (
    <div style={{ fontFamily: 'system-ui, Arial', padding: 20, maxWidth: 900, margin: '0 auto' }}>
      <h1 style={{ fontSize: 24, marginBottom: 8 }}>Evaluasi: Bangun Ruang Sisi Datar — 10 Soal (Pilihan Ganda + Alasan)</h1>
      <div style={{ marginBottom: 12 }}>
        <label style={{ marginRight: 8 }}>Peran:</label>
        <select value={role} onChange={e => setRole(e.target.value)}>
          <option value="student">Siswa</option>
          <option value="teacher">Guru</option>
        </select>
      </div>

      {role === 'student' && (
        <div>
          <div style={{ marginBottom: 12 }}>
            <input placeholder="Nama Siswa" value={name} onChange={e => setName(e.target.value)} style={{ marginRight: 8 }} />
            <input placeholder="Kelas" value={kelas} onChange={e => setKelas(e.target.value)} />
          </div>

          {QUESTIONS.map((q, i) => (
            <div key={q.id} style={{ padding: 12, border: '1px solid #ddd', borderRadius: 8, marginBottom: 12 }}>
              <div style={{ fontWeight: 600 }}>{q.id}. {q.text}</div>
              <div style={{ marginTop: 8 }}>
                {q.choices.map((c, ci) => (
                  <div key={ci} style={{ marginBottom: 6 }}>
                    <label>
                      <input type="radio" name={`q-${q.id}`} checked={answers[i].choice === ci} onChange={() => handleChoice(i, ci)} /> {' '}
                      {c}
                    </label>
                  </div>
                ))}
              </div>
              <div style={{ marginTop: 8 }}>
                <textarea placeholder="Tulis 1-2 kalimat alasan / strategi pemecahan (kritis)" value={answers[i].reason} onChange={e => handleReason(i, e.target.value)} style={{ width: '100%', minHeight: 60 }} />
              </div>
            </div>
          ))}

          <div style={{ marginTop: 8 }}>
            <button onClick={handleSubmit} style={{ padding: '8px 16px', borderRadius: 8 }}>Kirim & Unduh Hasil (Excel)</button>
            {submitted && (
              <div style={{ marginTop: 8 }}>
                <strong>Skor:</strong> {score} / {QUESTIONS.length}
              </div>
            )}
          </div>
        </div>
      )}

      {role === 'teacher' && (
        <div>
          <h2>Peran Guru</h2>
          <ol>
            <li>Host aplikasi (misal GitHub Pages / Netlify / Vercel) dan sebarkan tautan ke siswa.</li>
            <li>Minta siswa mengisi Nama dan Kelas sebelum mengerjakan.</li>
            <li>Terima file Excel hasil setiap siswa. File berisi jawaban pilihan serta kolom alasan siswa untuk menilai kemampuan berpikir kritis.</li>
            <li>Gunakan rubrik penilaian: 1) Ketepatan jawaban (benar/salah), 2) Kedalaman alasan (0-2), 3) Relevansi alasan (0-2). Jumlahkan untuk skor akhir.</li>
            <li>Simpan file dalam folder kelas dan susun agregat nilai bila perlu.</li>
          </ol>
          <h3>Template penilaian cepat (saran)</h3>
          <pre style={{ background: '#f7f7f7', padding: 8, borderRadius: 6 }}>
Ketepatan jawaban: 1 point per benar
Kedalaman alasan: 0 (kosong/tidak relevan), 1 (dangkal), 2 (mendalam)
Relevansi alasan: 0-2
Total per soal: 0-5
          </pre>
          <p>Jika guru ingin, saya bisa bantu membuat versi yang menyimpan banyak hasil ke satu file CSV/Excel (fitur kolaboratif) — beri tahu format yang diinginkan.</p>
        </div>
      )}

      <footer style={{ marginTop: 20, fontSize: 13, color: '#666' }}>
        Repo name suggestion: <strong>evaluasi-bangun-ruang-sisi-datar</strong>
        <br />Description suggestion: <em>Web app evaluasi 10 soal bangun ruang sisi datar untuk mengukur kemampuan berpikir kritis siswa; hasil diunduh sebagai Excel.</em>
      </footer>
    </div>
  );
}

// Mount for quick demo
const root = document.getElementById('root');
if (root) {
  createRoot(root).render(<App />);
}

export default App;
```

---

## Notes & next steps

- The code uses `xlsx` (SheetJS) to generate Excel files directly in the browser. When deploying, ensure `xlsx` is installed or included via CDN.
- The teacher/student workflow is intentionally lightweight: each student downloads their own Excel file which the teacher collects. For a centralized system, we'd need server-side endpoints and storage.

---

Happy to convert this into a full GitHub repo structure (separate files + `.gitignore`) and produce a downloadable ZIP, or push to a GitHub repo if you provide access/token. Tell me which you prefer next.
