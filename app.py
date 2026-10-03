from flask import Flask, render_template, request, jsonify
from pathlib import Path
from werkzeug.utils import secure_filename
from career_engine import extract_resume_text, analyze_resume, match_jobs, career_advice
from database import init_db, get_jobs

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / 'uploads'
UPLOAD_DIR.mkdir(exist_ok=True)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
init_db()

@app.get('/')
def index(): return render_template('index.html')

@app.get('/health')
def health(): return jsonify(status='ok', service='CareerLens AI')

@app.get('/api/jobs')
def jobs(): return jsonify(get_jobs())

@app.post('/api/analyze')
def analyze():
    if 'resume' not in request.files: return jsonify(error='Please upload a resume file.'), 400
    f=request.files['resume']
    if not f.filename: return jsonify(error='Please choose a resume file.'),400
    if not f.filename.lower().endswith(('.pdf','.txt')): return jsonify(error='Only PDF and TXT files are supported.'),400
    path=UPLOAD_DIR/secure_filename(f.filename); f.save(path)
    try:
        text=extract_resume_text(path)
        if len(text.strip())<30: return jsonify(error='The resume contains too little readable text.'),422
        return jsonify(analysis=analyze_resume(text), matches=match_jobs(text,get_jobs()), filename=path.name)
    except Exception as e: return jsonify(error=f'Could not analyze resume: {e}'),500
    finally: path.unlink(missing_ok=True)

@app.post('/api/advice')
def advice():
    data=request.get_json(silent=True) or {}; q=str(data.get('question','')).strip()
    if not q: return jsonify(error='Ask a career question first.'),400
    return jsonify(answer=career_advice(q,data.get('skills',[])))

if __name__=='__main__': app.run(debug=True)
