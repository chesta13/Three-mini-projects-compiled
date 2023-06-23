from flask import Flask, render_template, request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    keywords = [word for word in word_tokens if word.isalnum() and word not in stop_words]
    return keywords

def find_best_candidate(job_keywords, candidate_resumes):
    best_candidate = None
    best_match_count = 0

    for resume in candidate_resumes:
        resume_keywords = extract_keywords(resume)
        match_count = sum(keyword in resume_keywords for keyword in job_keywords)

        if match_count > best_match_count:
            best_match_count = match_count
            best_candidate = resume

    return best_candidate

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        job_description = request.form['job_description']
        num_candidates = int(request.form['num_candidates'])

        candidate_resumes = []
        for i in range(num_candidates):
            resume = request.form.get(f'resume_{i+1}', '')
            candidate_resumes.append(resume)

        job_keywords = extract_keywords(job_description)
        best_candidate_resume = find_best_candidate(job_keywords, candidate_resumes)

        return render_template('result.html', best_candidate_resume=best_candidate_resume)

    return render_template('form.html', num_candidates=5)  # Default number of candidates

if __name__ == '__main__':
    app.run(debug=True)

