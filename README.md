# evaluasi-bangun-ruang-sisi-datar

A Streamlit app for evaluating critical-thinking on flat-faced 3D shapes (bangun ruang sisi datar).
Features:
- 10 multiple-choice questions with real-life context.
- Students provide short justification per question (used for simple bonus scoring and teacher review).
- Results saved in-memory (demo) and downloadable as Excel per student.
- Teacher panel to view all responses and download aggregated Excel.

## Run locally
1. Clone repo
2. (Optional) create virtualenv
3. Install deps:
   pip install -r requirements.txt
4. Run:
   streamlit run app.py

## Notes for deployment
- For production, replace in-memory storage with DB (Google Sheets / Firebase / Postgres).
- Adjust scoring & rubrics for critical thinking as needed; current heuristic gives +0.5 point per justification ≥ 30 chars.
- Update questions / options in `app.py`.

License: MIT
