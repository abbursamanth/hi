import streamlit as st
import pandas as pd
import random

# Set page config
st.set_page_config(page_title="DBDA Course Recommendation")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("C://Users//Samanth Abbur//Desktop//deploy//udemy_courses.csv")

data = load_data()

def login_page():
    st.title("🔑 Login & Profile Setup")
    name = st.text_input("Enter your name:")
    interests = st.multiselect("Select your interests:", ["Web Development", "Business Finance", "Graphic Design", "Music"])
    if st.button("Save & Continue"):
        if name and interests:
            st.session_state["name"] = name
            st.session_state["interests"] = interests
            st.session_state["page"] = "dbda_test"
        else:
            st.warning("Please enter your name and select at least one interest.")

def dbda_test():
    st.title("🎯 DBDA Test")
    st.write("Answer 25 questions to determine your strongest domain!")
    
    # Define questions
    questions = {
        "Web Development": [
            {"question": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Hyper Tool Multi Language"], "answer": "Hyper Text Markup Language"},
            {"question": "Which language is used for styling web pages?", "options": ["CSS", "Python", "Java", "C++"], "answer": "CSS"},
            {"question": "Which of these is a JavaScript framework?", "options": ["React", "Django", "Flask", "Laravel"], "answer": "React"},
        ],
        "Business": [
            {"question": "What is the primary goal of a business?", "options": ["Maximize profits", "Increase expenses", "Reduce employee wages", "Avoid taxes"], "answer": "Maximize profits"},
            {"question": "What is the full form of KPI?", "options": ["Key Performance Indicator", "Key Product Insights", "Knowledge and Performance Index", "Key Process Improvement"], "answer": "Key Performance Indicator"},
            {"question": "Which is a common business strategy?", "options": ["Market Penetration", "Graphical Enhancement", "Audio Mixing", "Frontend Optimization"], "answer": "Market Penetration"},
        ],
        "Graphic Design": [
            {"question": "Which software is commonly used for graphic design?", "options": ["Photoshop", "Excel", "PowerPoint", "AutoCAD"], "answer": "Photoshop"},
            {"question": "What does DPI stand for in design?", "options": ["Dots Per Inch", "Design Process Index", "Digital Print Integration", "Depth of Pixel Interface"], "answer": "Dots Per Inch"},
            {"question": "Which color mode is used for printing?", "options": ["CMYK", "RGB", "Hex", "Grayscale"], "answer": "CMYK"},
        ],
        "Music": [
            {"question": "What are the seven basic musical notes?", "options": ["Do Re Mi Fa Sol La Ti", "A B C D E F G", "One Two Three Four Five Six Seven", "High Low Medium"], "answer": "Do Re Mi Fa Sol La Ti"},
            {"question": "Which of these is a string instrument?", "options": ["Guitar", "Trumpet", "Drums", "Flute"], "answer": "Guitar"},
            {"question": "What is a music scale?", "options": ["Series of musical notes in order", "A tool for measuring loudness", "A type of instrument", "A musical performance"], "answer": "Series of musical notes in order"},
        ],
    }
    
    responses = {}
    st.subheader("📝 Answer the following questions:")
    for idx, (domain, qlist) in enumerate(questions.items()):
        for q in qlist:
            responses[q["question"]] = st.radio(f"**{q['question']}**", q["options"])
    
    if st.button("Submit Answers"):
        domain_scores = {domain: 0 for domain in questions.keys()}
        
        for domain, qlist in questions.items():
            for q in qlist:
                if responses[q["question"]] == q["answer"]:
                    domain_scores[domain] += 1
        
        st.session_state["domain_scores"] = domain_scores
        st.session_state["page"] = "recommendation"

def recommendation():
    st.title("📊 Course Recommendation")
    domain_scores = st.session_state.get("domain_scores", {})
    strongest_domain = max(domain_scores, key=domain_scores.get)
    
    st.subheader("🔹 Your strongest domain:")
    st.write(f"**{strongest_domain}**")
    st.write("Domain scores:", domain_scores)
    
    # Recommend courses from dataset
    st.subheader("🎓 Recommended Courses")
    recommended_courses = data[data["subject"] == strongest_domain].head(5)
    st.write(recommended_courses[["course_title", "price", "num_subscribers"]])

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if st.session_state["page"] == "login":
    login_page()
elif st.session_state["page"] == "dbda_test":
    dbda_test()
elif st.session_state["page"] == "recommendation":
    recommendation()
