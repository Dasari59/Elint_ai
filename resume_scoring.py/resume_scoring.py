import os
import re
import csv
import PyPDF2
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to collect resumes from a folder
def collect_resumes(folder):
    return [file for file in Path(folder).glob("*.pdf")]  # Extend for DOCX if needed

# Function to extract text from PDF resumes
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text


# Function to score resumes against job description
def weighted_score_resume(resume_text, job_description):
    """Scores resumes based on weighted skills matching."""
    skills = {
        "Java": 40,
        "Spring Boot": 40,
        "MongoDB": 30,
        "PostgreSQL": 30,
        "Backend Development": 30
    }

    total_score = 0
    max_possible_score = sum(skills.values())  # Maximum possible score
    
    for skill, weight in skills.items():
        if skill.lower() in resume_text.lower():
            total_score += weight

    final_score = (total_score / max_possible_score) * 100
    return round(final_score, 2)

# Function to generate email feedback
def generate_email_template(name, score):
    if score >= 70:
        feedback = "Great match! You meet most requirements. Expect further communication soon."
    elif score >= 50:
        feedback = "You're close! Consider refining your skills or experience in key areas."
    else:
        feedback = "This role may not be the best fit right now. Keep improving your resume!"

    email_template = f"""
    Subject: Your Resume Evaluation Results

    Hi {name},

    Thank you for submitting your resume. We have evaluated your profile based on experience, skills, and relevance.

    **Your CV Score:** {score}%
    
    **Feedback:** {feedback}

    If you'd like to improve your match for future opportunities, consider enhancing your resume with additional skills, certifications, or work experience.

    Best regards,  
    AI Hiring Assistant  
    """
    return email_template

# Function to send automated email feedback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, name, score):
    sender_email = "dasarisaikalyan971@gmail.com"  # Replace with your actual email
    sender_password = "eeoa hnte yews gpxn"  # Consider using an App Password for Gmail

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = "Your Resume Evaluation Results"

    email_content = f"""
    Hi {name},

    Thank you for submitting your resume. We have evaluated your profile based on experience, skills, and relevance.

    **Your CV Score:** {score}%
    
    Feedback:
    - If score > 70%, you're a strong match!
    - If score 50-70%, consider improving some areas.
    - If score < 50%, refine skills or experience.

    Best regards,  
    AI Hiring Assistant  
    """
    
    msg.attach(MIMEText(email_content, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Ensure your email provider supports SMTP
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to: {to_email}")
    except Exception as e:
        print(f"⚠ Error sending email: {e}")

# Predefined list of candidate emails (Modify as needed)
candidate_emails = {
    "gauravsingh.pdf": "gauravsingh2356@gmail.com",
    "INDU.pdf": "indur96624555@gmail.com",
    "mohammad.pdf": "nadeemnawaz204455@gmail.com"
}

# Define job description for scoring
job_description = """Looking for a software engineer with expertise in Java, Spring Boot, and backend development.
Experience with databases like PostgreSQL, MongoDB, and OracleDB is preferred."""

# Define resume folder location
resume_folder = "C:\\Users\\DASARI SAI KALYAN\\OneDrive\\Desktop\\Resumes"
resume_files = collect_resumes(resume_folder)

print(f"Total Resumes Collected: {len(resume_files)}")

from datetime import datetime

log_file = "resume_log.csv"

def log_processed_resume(name, score, email_status):
    """Logs processed resumes to a CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = [timestamp, name, score, email_status]
    
    # Append data to CSV file
    with open(log_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(log_entry)

    print(f"📂 Logged: {name} | Score: {score}% | Email Sent: {email_status}")
# Process resumes and send feedback emails
for resume_path in resume_files:
    resume_text = extract_text_from_pdf(resume_path)
    cv_score = score_resume(resume_text, job_description)

    print(f"\nResume: {resume_path.name}")
    print(f"CV Match Score: {cv_score}%")

    if resume_path.name in candidate_emails:
        send_email(candidate_emails[resume_path.name], resume_path.name.split(".")[0], cv_score)
    else:
        print("No predefined email found for this resume.")

    