import sqlite3
from pathlib import Path
DB_PATH=Path(__file__).resolve().parent/'careerlens.db'
SEED=[
('Python Developer','Build Python applications, APIs and automation tools.','Python, Flask, SQL, Git, REST API, OOP','Software'),
('Data Analyst','Analyze business data and communicate actionable insights.','Python, SQL, Pandas, Statistics, Excel, Power BI, Data Visualization','Data'),
('Machine Learning Intern','Prepare datasets and develop machine learning models.','Python, Pandas, NumPy, Scikit-learn, Machine Learning, Statistics, SQL','AI/ML'),
('Frontend Developer','Create responsive and accessible web interfaces.','HTML, CSS, JavaScript, Responsive Design, Git, REST API','Web'),
('Full Stack Developer','Develop end-to-end web applications.','HTML, CSS, JavaScript, Python, Flask, SQL, REST API, Git','Web'),
('AI Engineer Intern','Prototype AI features and integrate intelligent systems.','Python, Machine Learning, NLP, APIs, SQL, Git','AI/ML')]
def connect():
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_db():
    with connect() as c:
        c.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,description TEXT,skills TEXT,category TEXT)')
        if c.execute('SELECT COUNT(*) FROM jobs').fetchone()[0]==0: c.executemany('INSERT INTO jobs(title,description,skills,category) VALUES(?,?,?,?)',SEED)
def get_jobs():
    with connect() as c: return [dict(r) for r in c.execute('SELECT id,title,description,skills,category FROM jobs ORDER BY id')]
