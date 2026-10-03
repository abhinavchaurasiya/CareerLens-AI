from pathlib import Path
import math,re
ALIASES={'python':['python'],'java':['java'],'c++':['c++','cpp'],'html':['html','html5'],'css':['css','css3'],'javascript':['javascript','js'],'react':['react','react.js','reactjs'],'flask':['flask'],'django':['django'],'sql':['sql','mysql','postgresql','sqlite'],'git':['git','github','version control'],'rest api':['rest api','restful','api development'],'pandas':['pandas'],'numpy':['numpy'],'scikit-learn':['scikit-learn','sklearn'],'machine learning':['machine learning',' ml '],'deep learning':['deep learning'],'nlp':['nlp','natural language processing'],'statistics':['statistics','statistical'],'excel':['excel'],'power bi':['power bi'],'data visualization':['data visualization','data visualisation'],'responsive design':['responsive design','responsive web'],'oop':['oop','object oriented','object-oriented']}
def extract_resume_text(path:Path):
    if path.suffix.lower()=='.txt': return path.read_text(encoding='utf-8',errors='ignore')
    if path.suffix.lower()=='.pdf':
        from pypdf import PdfReader
        return '\n'.join(p.extract_text() or '' for p in PdfReader(str(path)).pages)
    raise ValueError('Unsupported file type')
def norm(s): return re.sub(r'\s+',' ',s.lower()).strip()
def extract_skills(text):
    t=norm(text); out=[]
    for skill,aliases in ALIASES.items():
        if any((re.search(a,t) if any(ch in a for ch in r'\[]().*+?^$|') else a in t) for a in aliases) and skill not in out: out.append(skill)
    return sorted(out)
def tokens(s): return re.findall(r'[a-zA-Z][a-zA-Z0-9+#.-]*',norm(s))
def cosine(a,b):
    A=tokens(a);B=tokens(b); fa={};fb={}
    for x in A: fa[x]=fa.get(x,0)+1
    for x in B: fb[x]=fb.get(x,0)+1
    common=set(fa)&set(fb); n=sum(fa[x]*fb[x] for x in common); da=math.sqrt(sum(v*v for v in fa.values()));db=math.sqrt(sum(v*v for v in fb.values()))
    return n/(da*db) if da and db else 0
def match_jobs(text,jobs):
    rs=set(extract_skills(text)); result=[]
    for j in jobs:
        req=set(extract_skills(j['skills'])); matched=sorted(rs&req); missing=sorted(req-rs)
        skill=len(matched)/len(req) if req else 0; semantic=cosine(text,j['title']+' '+j['description']+' '+j['skills']); score=max(0,min(100,round((skill*.75+semantic*.25)*100)))
        result.append({'id':j['id'],'title':j['title'],'category':j['category'],'score':score,'matched_skills':matched,'missing_skills':missing})
    return sorted(result,key=lambda x:x['score'],reverse=True)
def analyze_resume(text):
    skills=extract_skills(text); sections=[x.title() for x in ['education','experience','projects','skills','certifications'] if re.search(r'\b'+x+r'\b',text,re.I)]
    score=min(100,45+min(len(skills)*5,35)+min(len(sections)*4,20))
    return {'skills':skills,'skill_count':len(skills),'word_count':len(tokens(text)),'detected_sections':sections,'project_mentions':len(re.findall(r'\bprojects?\b',text,re.I)),'profile_score':score}
def career_advice(q,skills):
    q=norm(q); s=', '.join(skills) if skills else 'your current skills'
    if 'data' in q: return f'With {s}, focus next on SQL, statistics, Pandas, data visualization and machine learning. Build 2–3 projects and document the results.'
    if any(x in q for x in ['web','frontend','full stack']): return f'With {s}, strengthen JavaScript, responsive UI, REST APIs, Git and a Python backend such as Flask. Build one complete deployed application.'
    if any(x in q for x in ['machine learning',' ml ','ai']): return f'Your AI/ML path can be Python → NumPy/Pandas → statistics → scikit-learn → model evaluation → deployment. Start with a classification or regression project.'
    if any(x in q for x in ['resume','cv']): return 'Keep the resume concise, quantify project outcomes, list technologies beside each project, and put your strongest project near the top.'
    if any(x in q for x in ['interview','placement','job']): return 'Prepare DSA basics, SQL, OOP, one strong project you can explain end-to-end, and common behavioral questions.'
    return f'Start from {s}, choose one target role, identify 3–5 missing skills, build a project using them, and document it on GitHub.'
