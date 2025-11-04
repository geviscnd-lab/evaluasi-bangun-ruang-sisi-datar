/*
Repository name: evaluasi-bangun-datar-sisi-datar
Description: A lightweight single-file React app that delivers 10 real-life multiple-choice questions about flat shapes (bangun datar sisi datar) to assess students' critical-thinking in problem solving. It collects answers, optional short justifications, and exports the student's work as an Excel/CSV file for teachers to review.

What this file contains:
- A complete React component (default export) that can be used as App.jsx in a Create React App / Vite React project.
- 10 MCQ in Indonesian with real-life contexts.
- Optional short-justification fields so students can explain their reasoning (for critical thinking assessment).
- CSV export (download) of the student's responses and metadata.
- Simple scoring and feedback.

Peran guru dan siswa (ringkasan):
- Peran Guru:
  1. Menyajikan pre-test dan instruksi (tujuan: mengukur kemampuan berpikir kritis pada konteks kehidupan sehari-hari).
  2. Memfasilitasi: menjelaskan format soal, waktu pengerjaan, dan cara mengisi kolom penjelasan singkat.
  3. Mengunduh file hasil (Excel/CSV) dan menilai aspek kualitatif dari penjelasan siswa (rubrik berpikir kritis: kejelasan premis, penggunaan fakta/konsep, kesimpulan logis, kreativitas solusi).
  4. Memberi umpan balik individu/kelompok berdasarkan skor kuantitatif dan analisis kualitatif jawaban.

- Peran Siswa:
  1. Membaca setiap soal dengan teliti dan memilih jawaban terbaik berdasarkan konteks.
  2. Mengisi singkat alasan/penjelasan untuk setiap soal (minimal 1-2 kalimat) untuk menunjukkan proses berpikir.
  3. Menyelesaikan seluruh soal, meninjau jawaban, lalu menekan tombol "Kirim & Unduh Hasil" untuk menghasilkan file Excel/CSV.
  4. Menerima dan merefleksikan umpan balik guru untuk memperbaiki strategi pemecahan masalah.

Instruksi singkat penggunaan (copy ke App.jsx):
1. Buat project React (Create React App atau Vite).
2. Tempelkan file ini sebagai src/App.jsx.
3. Jalankan proyek dengan `npm install` dan `npm start` (atau `npm run dev` untuk Vite).
4. Buka halaman, isi nama & kelas, kerjakan soal, lalu klik tombol untuk mengunduh hasil.

*/

import React, { useState } from 'react';

const QUESTIONS = [
  {
    id: 1,
    text: 'Seorang tukang roti ingin memotong kertas pembungkus berbentuk persegi panjang menjadi beberapa kotak persegi sama besar untuk membungkus roti. Jika ukuran kertas 60 cm x 40 cm, berapa ukuran sisi kotak persegi maksimum agar tidak tersisa kertas?
    (Pilih jawaban yang benar)',
    choices: [
      '10 cm',
      '20 cm',
      '30 cm',
      '40 cm'
    ],
    answer: 1 // index (0-based): 1 -> '20 cm'
  },
  {
    id: 2,
    text: 'Seorang petani ingin membuat pagar berbentuk segiempat untuk kebun dengan luas 72 m². Jika salah satu sisi panjangnya 12 m, berapa lebar kebun tersebut? (Aplikasi kehidupan sehari-hari)',
    choices: [
      '4 m',
      '5 m',
      '6 m',
      '8 m'
    ],
    answer: 2
  },
  {
    id: 3,
    text: 'Sebuah meja berbentuk persegi panjang memiliki panjang 150 cm dan lebar 80 cm. Untuk menutup meja dengan kain, berapa luas kain yang diperlukan dalam meter persegi (m²)?',
    choices: [
      '1.2 m²',
      '12 m²',
      '1.5 m²',
      '0.72 m²'
    ],
    answer: 0
  },
  {
    id: 4,
    text: 'Seorang desainer ingin membuat mozaik berbentuk segitiga sama sisi dengan sisi 10 cm. Berapakah keliling satu mozaik segitiga tersebut?',
    choices: [
      '10 cm',
      '20 cm',
      '30 cm',
      '40 cm'
    ],
    answer: 2
  },
  {
    id: 5,
    text: 'Sebuah taman kota berbentuk lingkaran memiliki radius 7 meter. Ibu-ibu komunitas ingin menanam pagar bunga di sepanjang keliling taman. Berapa panjang keliling yang harus mereka tanami? (Gunakan π ≈ 22/7)',
    choices: [
      '14 m',
      '44 m',
      '154 m',
      '88 m'
    ],
    answer: 1
  },
  {
    id: 6,
    text: 'Sebuah papan reklame berbentuk trapesium dengan panjang sisi sejajar 8 m dan 5 m, serta tinggi 3 m. Berapa luas papan reklame tersebut?',
    choices: [
      '19.5 m²',
      '13.5 m²',
      '39 m²',
      '20 m²'
    ],
    answer: 0
  },
  {
    id: 7,
    text: 'Seorang tukang kayu akan membuat kotak dari papan berbentuk persegi dengan sisi 25 cm. Namun, ia ingin mengetahui berapa luas permukaan atas kotak (satu sisi). Berapa luas sisi atasnya?',
    choices: [
      '625 cm²',
      '100 cm²',
      '2500 cm²',
      '125 cm²'
    ],
    answer: 0
  },
  {
    id: 8,
    text: 'Sebuah lantai kamar mandi berbentuk persegi panjang 2,5 m x 1,6 m akan dipasang keramik persegi ukuran 20 cm x 20 cm. Berapa banyak keramik yang diperlukan (asumsikan tidak ada potongan)?',
    choices: [
      '200 buah',
      '125 buah',
      '50 buah',
      '100 buah'
    ],
    answer: 3
  },
  {
    id: 9,
    text: 'Seorang pengrajin ingin memotong kain berbentuk persegi panjang menjadi beberapa segitiga siku-siku yang sama besar untuk membuat patchwork. Jika kain berukuran 120 cm x 80 cm setiap segitiga didapat dari memotong persegi 40 cm x 40 cm menjadi dua segitiga, berapa jumlah segitiga yang didapat?',
    choices: [
      '48',
      '24',
      '12',
      '96'
    ],
    answer: 0
  },
  {
    id: 10,
    text: 'Sebuah pintu kamar berbentuk persegi panjang 210 cm x 80 cm ingin dicat. Jika cat menutup 1 liter untuk 6 m², berapa liter cat yang diperlukan? (Pembulatan ke dua desimal)',
    choices: [
      '0.34 L',
      '1.68 L',
      '2.80 L',
      '0.28 L'
    ],
    answer: 1
  }
];

export default function App() {
  const [name, setName] = useState('');
  const [className, setClassName] = useState('');
  const [answers, setAnswers] = useState(() => QUESTIONS.map(() => null));
  const [explanations, setExplanations] = useState(() => QUESTIONS.map(() => ''));
  const [submitted, setSubmitted] = useState(false);

  function handleChoiceChange(qIndex, choiceIndex) {
    const next = [...answers];
    next[qIndex] = choiceIndex;
    setAnswers(next);
  }

  function handleExplanationChange(qIndex, text) {
    const next = [...explanations];
    next[qIndex] = text;
    setExplanations(next);
  }

  function score() {
    let correct = 0;
    for (let i = 0; i < QUESTIONS.length; i++) {
      if (answers[i] === QUESTIONS[i].answer) correct++;
    }
    return { total: QUESTIONS.length, correct, percent: Math.round((correct / QUESTIONS.length) * 100) };
  }

  function buildCSV() {
    const header = [
      'Nama', 'Kelas', 'Tanggal', 'Soal ID', 'Soal', 'Jawaban Pilihan', 'Jawaban Benar', 'Benar?', 'Penjelasan Singkat'
    ];

    const rows = [];
    const now = new Date().toLocaleString();
    for (let i = 0; i < QUESTIONS.length; i++) {
      rows.push([
        name,
        className,
        now,
        QUESTIONS[i].id,
        QUESTIONS[i].text.replace(/\n/g, ' '),
        answers[i] != null ? QUESTIONS[i].choices[answers[i]] : '',
        QUESTIONS[i].choices[QUESTIONS[i].answer],
        answers[i] === QUESTIONS[i].answer ? 'YA' : 'TIDAK',
        explanations[i].replace(/\n/g, ' ')
      ]);
    }

    // Also include summary row
    const s = score();
    rows.push(['', '', '', 'SUMMARY', `Benar: ${s.correct}/${s.total}`, `Persen: ${s.percent}%`, '', '', '']);

    // Convert to CSV
    const csvParts = [];
    csvParts.push(header.join(','));
    for (const r of rows) {
      // Escape double quotes
      const escaped = r.map(cell => '"' + String(cell).replace(/"/g, '""') + '"');
      csvParts.push(escaped.join(','));
    }
    return csvParts.join('\n');
  }

  function downloadCSV() {
    if (!name || !className) {
      alert('Silakan isi Nama dan Kelas sebelum mengunduh hasil.');
      return;
    }
    const csv = buildCSV();
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const safeName = name.replace(/[^a-z0-9_\-]/gi, '_');
    a.download = `${safeName}_${className}_hasil_bangun_datar.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function handleSubmit(e) {
    e.preventDefault();
    setSubmitted(true);
    // Auto-download after submit
    setTimeout(() => downloadCSV(), 300);
  }

  const s = score();

  return (
    <div className="min-h-screen p-6 bg-gray-50">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-2xl shadow">
        <h1 className="text-2xl font-bold mb-2">Evaluasi: Bangun Datar (Sisi-datar) — 10 Soal Pilihan Ganda</h1>
        <p className="text-sm mb-4">Tujuan: Mengukur kemampuan berpikir kritis siswa dalam menyelesaikan soal berkonteks kehidupan sehari-hari.</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex gap-4">
            <input required value={name} onChange={(e) => setName(e.target.value)} placeholder="Nama siswa" className="flex-1 p-2 border rounded" />
            <input required value={className} onChange={(e) => setClassName(e.target.value)} placeholder="Kelas" className="w-40 p-2 border rounded" />
          </div>

          {QUESTIONS.map((q, qi) => (
            <div key={q.id} className="p-4 border rounded">
              <div className="font-medium">Soal {qi + 1}. {q.text}</div>
              <div className="mt-2 space-y-1">
                {q.choices.map((ch, ci) => (
                  <label key={ci} className="flex items-center gap-2">
                    <input
                      type="radio"
                      name={`q_${q.id}`}
                      checked={answers[qi] === ci}
                      onChange={() => handleChoiceChange(qi, ci)}
                    />
                    <span>{String.fromCharCode(65 + ci)}. {ch}</span>
                  </label>
                ))}
              </div>
              <div className="mt-2">
                <label className="text-sm">Penjelasan singkat (1-2 kalimat) — tuliskan alasan pilihan Anda untuk menilai kemampuan berpikir kritis:</label>
                <textarea value={explanations[qi]} onChange={(e) => handleExplanationChange(qi, e.target.value)} rows={2} className="w-full p-2 border rounded mt-1" placeholder="Tuliskan alasan singkat..." />
              </div>
            </div>
          ))}

          <div className="flex gap-3">
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">Kirim & Unduh Hasil</button>
            <button type="button" onClick={() => { setAnswers(QUESTIONS.map(() => null)); setExplanations(QUESTIONS.map(() => '')); setSubmitted(false); }} className="px-4 py-2 border rounded">Reset</button>
            <button type="button" onClick={() => { setSubmitted(true); downloadCSV(); }} className="px-4 py-2 border rounded">Unduh tanpa kirim</button>
          </div>
        </form>

        {submitted && (
          <div className="mt-6 p-4 bg-gray-100 rounded">
            <h2 className="font-semibold">Ringkasan Hasil</h2>
            <p>Nilai: {s.correct} / {s.total} ({s.percent}%)</p>
            <p className="text-sm mt-2">Catatan untuk guru: unduh CSV untuk menilai penjelasan singkat siswa dan gunakan rubrik berpikir kritis (kejelasan, penggunaan konsep, kebenaran langkah, kesimpulan).</p>
          </div>
        )}

        <details className="mt-6 text-sm text-gray-600">
          <summary className="cursor-pointer">Panduan singkat: cara menilai penjelasan (rubrik)</summary>
          <ol className="mt-2 pl-4 list-decimal">
            <li>Kejelasan premise & tujuan (0-2): apakah siswa menjelaskan apa yang dicari?</li>
            <li>Penerapan konsep (0-2): apakah siswa menggunakan konsep bangun datar secara benar?</li>
            <li>Kejelasan langkah/logika (0-2): apakah alur pemecahan masalah dapat dipahami?</li>
            <li>Kreativitas & relevansi solusi (0-2): solusi efektif dan sesuai konteks?</li>
            <li>Konsistensi jawaban & perhitungan (0-2): jawaban benar atau beralasan jika salah?</li>
          </ol>
        </details>

      </div>

      <footer className="max-w-4xl mx-auto mt-4 text-xs text-gray-500">Repository: evaluasi-bangun-datar-sisi-datar • Buat di local dan unggah ke GitHub. (File ini siap ditempel di src/App.jsx)</footer>
    </div>
  );
}
