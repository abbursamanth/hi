import streamlit as st

# Set page title
st.set_page_config(page_title="DBDA Course Recommendation Test")

st.title("🎯 Domain-Based Diagnostic Assessment (DBDA) Test")
st.write("Answer 25 questions to determine your strongest domain: Web Development, Business, Graphic Design, or Music.")

# Define questions categorized by domain
questions = {
    "Web Development": [
        {"question": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Hyper Tool Multi Language"], "answer": "Hyper Text Markup Language"},
        {"question": "Which language is used for styling web pages?", "options": ["CSS", "Python", "Java", "C++"], "answer": "CSS"},
        {"question": "Which of these is a JavaScript framework?", "options": ["React", "Django", "Flask", "Laravel"], "answer": "React"},
        {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Server Query Language", "System Query Logic", "Sequential Query Language"], "answer": "Structured Query Language"},
        {"question": "Which protocol is used for secure data transfer on the web?", "options": ["HTTP", "FTP", "HTTPS", "TCP"], "answer": "HTTPS"},
    ],
    "Business": [
        {"question": "What is the primary goal of a business?", "options": ["Maximize profits", "Increase expenses", "Reduce employee wages", "Avoid taxes"], "answer": "Maximize profits"},
        {"question": "What is the full form of KPI?", "options": ["Key Performance Indicator", "Key Product Insights", "Knowledge and Performance Index", "Key Process Improvement"], "answer": "Key Performance Indicator"},
        {"question": "Which is a common business strategy?", "options": ["Market Penetration", "Graphical Enhancement", "Audio Mixing", "Frontend Optimization"], "answer": "Market Penetration"},
        {"question": "What does ROI stand for?", "options": ["Return on Investment", "Rate of Interest", "Revenue on Income", "Reimbursement of Investment"], "answer": "Return on Investment"},
        {"question": "Which financial statement shows a company’s profitability?", "options": ["Balance Sheet", "Cash Flow Statement", "Income Statement", "Tax Report"], "answer": "Income Statement"},
    ],
    "Graphic Design": [
        {"question": "Which software is commonly used for graphic design?", "options": ["Photoshop", "Excel", "PowerPoint", "AutoCAD"], "answer": "Photoshop"},
        {"question": "What does DPI stand for in design?", "options": ["Dots Per Inch", "Design Process Index", "Digital Print Integration", "Depth of Pixel Interface"], "answer": "Dots Per Inch"},
        {"question": "Which color mode is used for printing?", "options": ["CMYK", "RGB", "Hex", "Grayscale"], "answer": "CMYK"},
        {"question": "Which tool is used for vector graphics?", "options": ["Illustrator", "Photoshop", "Excel", "Premiere Pro"], "answer": "Illustrator"},
        {"question": "What is a logo?", "options": ["A visual identity mark", "A business license", "A product description", "A social media post"], "answer": "A visual identity mark"},
    ],
    "Music": [
        {"question": "What are the seven basic musical notes?", "options": ["Do Re Mi Fa Sol La Ti", "A B C D E F G", "One Two Three Four Five Six Seven", "High Low Medium"], "answer": "Do Re Mi Fa Sol La Ti"},
        {"question": "Which of these is a string instrument?", "options": ["Guitar", "Trumpet", "Drums", "Flute"], "answer": "Guitar"},
        {"question": "What is a music scale?", "options": ["Series of musical notes in order", "A tool for measuring loudness", "A type of instrument", "A musical performance"], "answer": "Series of musical notes in order"},
        {"question": "What is tempo in music?", "options": ["Speed of the beat", "Type of instrument", "Loudness of sound", "Musical genre"], "answer": "Speed of the beat"},
        {"question": "Which instrument is commonly used in orchestras?", "options": ["Violin", "Electric Guitar", "Synthesizer", "Saxophone"], "answer": "Violin"},
    ],
}

# Collect all questions in a list
all_questions = []
for domain in questions.keys():
    all_questions.extend(questions[domain])

# Dictionary to store user responses
responses = {}

# Display questions
st.subheader("📝 Answer the following questions:")
for idx, q in enumerate(all_questions):
    responses[idx] = st.radio(f"**{idx + 1}. {q['question']}**", q["options"])

# Submit button
if st.button("Submit Answers"):
    # Scoring system
    domain_scores = {"Web Development": 0, "Business": 0, "Graphic Design": 0, "Music": 0}

    # Evaluate correct answers
    for idx, q in enumerate(all_questions):
        if responses[idx] == q["answer"]:
            for domain, question_list in questions.items():
                if q in question_list:
                    domain_scores[domain] += 1

    # Determine strongest domain
    strongest_domain = max(domain_scores, key=domain_scores.get)

    # Display results
    st.subheader("🎉 Test Results:")
    st.write(f"**Your strongest domain is: {strongest_domain}**")
    st.write("Domain scores:", domain_scores)

    # Course recommendation
    st.subheader("📚 Course Recommendation:")
    courses = {
        "Web Development": ["Full-Stack Web Development with React", "JavaScript for Beginners", "Python Django Web App Development"],
        "Business": ["Business Analytics Masterclass", "Entrepreneurship Bootcamp", "Marketing Strategies for Growth"],
        "Graphic Design": ["Adobe Photoshop Mastery", "Illustrator for Beginners", "UI/UX Design Fundamentals"],
        "Music": ["Guitar Masterclass", "Piano for Beginners", "Music Theory Essentials"]
    }

    # Recommend based on the strongest domain
    recommended_course = courses[strongest_domain][0]  # Pick the most relevant course
    st.write(f"🔹 **Recommended Course: {recommended_course}**")
