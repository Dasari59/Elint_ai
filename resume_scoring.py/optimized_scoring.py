import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# Load NLP model for better keyword matching
nlp = spacy.load("en_core_web_sm")  

# Function to extract years of experience from resume text
def extract_experience(text):
    match = re.search(r'(\d+)\s*(?:years|yrs|year)', text, re.IGNORECASE)
    return int(match.group(1)) if match else 0  # Default to 0 if no match found

# Improved scoring function
def score_resume(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0] * 100
    
    # Extract experience from resume
    experience_years = extract_experience(resume_text)
    experience_score = min(20, experience_years * 2)  # Capping experience points at 20
    
    # Final adjusted score
    final_score = round(similarity + experience_score, 2)
    
    return final_score

# Sample resume and job description for testing
resume_sample = "AI Engineer skilled in Python, NLP, ML with 5 years of experience."
job_description = "Looking for an AI engineer with expertise in Python, NLP, and Machine Learning."

# Running the scoring function
cv_score = score_resume(resume_sample, job_description)
print(f"Optimized CV Match Score: {cv_score}%")