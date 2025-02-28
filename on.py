import streamlit as st

# Define courses
courses = {
    "Web Development": [
        "Full-Stack Web Development with React", 
        "JavaScript for Beginners", 
        "Python Django Web App Development"
    ],
    "Business": [
        "Business Analytics Masterclass", 
        "Entrepreneurship Bootcamp", 
        "Marketing Strategies for Growth"
    ],
    "Graphic Design": [
        "Adobe Photoshop Mastery", 
        "Illustrator for Beginners", 
        "UI/UX Design Fundamentals"
    ],
    "Music": [
        "Guitar Masterclass", 
        "Piano for Beginners", 
        "Music Theory Essentials"
    ]
}

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

# Session state variables
if "page" not in st.session_state:
    st.session_state.page = "login"
if "name" not in st.session_state:
    st.session_state.name = ""
if "interests" not in st.session_state:
    st.session_state.interests = []
if "responses" not in st.session_state:
    st.session_state.responses = {}

# Login Page
if st.session_state.page == "login":
    st.title("🎓 Welcome to DBDA Course Recommendation")
    st.subheader("🔑 Login")

    st.session_state.name = st.text_input("Enter your name:")
    st.session_state.interests = st.multiselect("Select your interests:", ["Web Development", "Business", "Graphic Design", "Music"])

    if st.button("Start Test"):
        if st.session_state.name and st.session_state.interests:
            st.session_state.page = "test"
            st.rerun()
        else:
            st.warning("Please enter your name and select at least one interest.")

# DBDA Test Page
elif st.session_state.page == "test":
    st.title(f"📝 DBDA Test for {st.session_state.name}")
    
    st.write("Answer the following questions:")
    question_idx = 0
    for domain, question_list in questions.items():
        for q in question_list:
            st.session_state.responses[question_idx] = st.radio(f"**{question_idx + 1}. {q['question']}**", q["options"], key=question_idx)
            question_idx += 1

    if st.button("Submit Answers"):
        st.session_state.page = "result"
        st.rerun()

# Result Page
elif st.session_state.page == "result":
    st.title("🎯 Test Results")

    # Scoring system
    domain_scores = {domain: 0 for domain in questions}
    
    question_idx = 0
    for domain, question_list in questions.items():
        for q in question_list:
            if st.session_state.responses.get(question_idx) == q["answer"]:
                domain_scores[domain] += 1
            question_idx += 1

    # Determine strengths
    strongest_domain = max(domain_scores, key=domain_scores.get)
    
    # Show results
    st.write(f"**Your strongest domain is: {strongest_domain}**")
    st.write("### Detailed Scores:")
    for domain, score in domain_scores.items():
        st.write(f"- **{domain}:** {score} correct answers")

    # Course Recommendations
    st.subheader("📚 Recommended Courses")
    for domain in st.session_state.interests:
        if domain in domain_scores:
            st.write(f"**{domain} Courses:**")
            for course in courses[domain]:
                st.write(f"- {course}")

    st.button("Restart", on_click=lambda: st.session_state.update(page="login", responses={}, name="", interests=[]))
