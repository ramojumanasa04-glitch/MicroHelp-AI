import re
from datetime import datetime
import streamlit as st
st.set_page_config(
    page_title="MicroHelp AI",
    page_icon="🤝",
    layout="wide",
)
if "requests" not in st.session_state:
    st.session_state.requests = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
SKILL_KEYWORDS = {
    "Python Programming": [
        "python",
        "programming",
        "code",
        "coding",
        "error",
        "bug",
        "function",
        "program",
    ],
    "Web Development": [
        "website",
        "web",
        "html",
        "css",
        "javascript",
        "frontend",
        "backend",
        "webpage",
    ],
    "Database / SQL": [
        "database",
        "sql",
        "mysql",
        "dbms",
        "query",
        "table",
        "database error",
    ],
    "Java Programming": [
        "java",
        "class",
        "object",
        "inheritance",
        "exception",
        "thread",
        "oops",
    ],
    "Computer Hardware": [
        "laptop",
        "computer",
        "keyboard",
        "mouse",
        "printer",
        "screen",
        "hardware",
        "wifi",
    ],
    "Academic Help": [
        "exam",
        "assignment",
        "notes",
        "subject",
        "study",
        "college",
        "semester",
        "question",
    ],
    "Design / UI": [
        "design",
        "ui",
        "ux",
        "figma",
        "logo",
        "poster",
        "interface",
    ],
}
HELPER_TYPES = {
    "Python Programming": "Python Developer / Programming Mentor",
    "Web Development": "Web Developer",
    "Database / SQL": "Database / SQL Expert",
    "Java Programming": "Java Developer / OOP Mentor",
    "Computer Hardware": "Computer Hardware Technician",
    "Academic Help": "Student Mentor / Academic Tutor",
    "Design / UI": "UI/UX Designer",
    "General": "General Helper",
}
def clean_text(text):
    """Convert text into simple normalized words."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    return text
def detect_skill(problem):
    """
    Detect the most relevant skill using keyword matching.
    Returns skill and matching keywords.
    """
    cleaned_problem = clean_text(problem)
    scores = {}
    for skill, keywords in SKILL_KEYWORDS.items():
        score = 0
        matched = []
        for keyword in keywords:
            if keyword.lower() in cleaned_problem:
                score += 1
                matched.append(keyword)
        scores[skill] = {
            "score": score,
            "matched": matched,
        }
    best_skill = max(
        scores,
        key=lambda skill: scores[skill]["score"]
    )
    if scores[best_skill]["score"] == 0:
        return "General", []
    return best_skill, scores[best_skill]["matched"]
def get_priority(problem):
    """Estimate request priority."""
    urgent_words = [
        "urgent",
        "emergency",
        "immediately",
        "asap",
        "important",
        "deadline",
        "tomorrow",
    ]
    cleaned_problem = clean_text(problem)
    for word in urgent_words:
        if word in cleaned_problem:
            return "High"
    return "Normal"
with st.sidebar:
    st.title("🤝 MicroHelp AI")
    st.write(
        "Connect people who need small everyday help "
        "with people who have the right skills."
    )
    st.divider()
    st.subheader("👤 Your Profile")
    st.session_state.user_name = st.text_input(
        "Your name",
        value=st.session_state.user_name,
        placeholder="Enter your name",
    )
    st.divider()
    st.subheader("📊 Platform Statistics")
    st.metric(
        "Help Requests",
        len(st.session_state.requests),
    )
    resolved = sum(
        1
        for request in st.session_state.requests
        if request["status"] == "Resolved"
    )
    st.metric(
        "Resolved",
        resolved,
    )
st.title("🤝 MicroHelp AI")
st.subheader(
    "Small problem? Find the right person to help."
)
st.write(
    "Describe your problem in simple words. "
    "MicroHelp AI identifies the skill you need and "
    "suggests the right type of helper."
)
st.divider()
tab1, tab2, tab3 = st.tabs(
    [
        "🆘 Ask for Help",
        "📋 Help Requests",
        "ℹ️ About",
    ]
)
with tab1:
    st.header("🆘 What do you need help with?")
    problem = st.text_area(
        "Describe your problem",
        height=160,
        placeholder=(
            "Example: My Python program is showing an error "
            "when I try to read a file."
        ),
    )
    category = st.selectbox(
        "Optional category",
        [
            "Let AI identify",
            "Python Programming",
            "Web Development",
            "Database / SQL",
            "Java Programming",
            "Computer Hardware",
            "Academic Help",
            "Design / UI",
            "General",
        ],
    )
    if st.button(
        "🔍 Analyze My Problem",
        type="primary",
        use_container_width=True,
    ):
        if not problem.strip():
            st.warning(
                "Please describe your problem first."
            )
        else:
            if category == "Let AI identify":
                skill, matched_keywords = detect_skill(problem)
            else:
                skill = category
                matched_keywords = []
            helper = HELPER_TYPES.get(
                skill,
                HELPER_TYPES["General"],
            )
            priority = get_priority(problem)
            st.success("Problem analyzed successfully!")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Required Skill",
                    skill,
                )
            with col2:
                st.metric(
                    "Suggested Helper",
                    helper,
                )
            with col3:
                st.metric(
                    "Priority",
                    priority,
                )
            if matched_keywords:
                st.write(
                    "**Detected keywords:** "
                    + ", ".join(matched_keywords)
                )
            st.info(
                f"💡 You should connect with a **{helper}** "
                f"for this problem."
            )
            st.session_state.last_analysis = {
                "problem": problem,
                "skill": skill,
                "helper": helper,
                "priority": priority,
            }
    if "last_analysis" in st.session_state:
        st.divider()
        st.subheader("📨 Create Help Request")
        analysis = st.session_state.last_analysis
        if st.button(
            "🚀 Send Help Request",
            use_container_width=True,
        ):
            request = {
                "id": len(st.session_state.requests) + 1,
                "user": (
                    st.session_state.user_name
                    if st.session_state.user_name
                    else "Anonymous User"
                ),
                "problem": analysis["problem"],
                "skill": analysis["skill"],
                "helper": analysis["helper"],
                "priority": analysis["priority"],
                "status": "Open",
                "created": datetime.now().strftime(
                    "%d-%m-%Y %I:%M %p"
                ),
            }
            st.session_state.requests.append(request)
            st.success(
                "Your help request has been created!"
            )
with tab2:
    st.header("📋 Help Requests")
    if not st.session_state.requests:
        st.info(
            "No help requests yet. "
            "Create your first request from the "
            "'Ask for Help' tab."
        )
    else:
        for request in reversed(
            st.session_state.requests
        ):
            with st.container(border=True):
                col1, col2 = st.columns(
                    [4, 1]
                )
                with col1:
                    st.subheader(
                        f"Request #{request['id']}"
                    )
                    st.write(
                        f"**User:** {request['user']}"
                    )
                    st.write(
                        f"**Problem:** {request['problem']}"
                    )
                    st.write(
                        f"**Required Skill:** "
                        f"{request['skill']}"
                    )
                    st.write(
                        f"**Suggested Helper:** "
                        f"{request['helper']}"
                    )
                    st.caption(
                        f"Created: {request['created']}"
                    )
                with col2:
                    if request["priority"] == "High":
                        st.error(
                            f"🔥 {request['priority']} Priority"
                        )
                    else:
                        st.info(
                            f"🟢 {request['priority']} Priority"
                        )
                    st.write(
                        f"Status: **{request['status']}**"
                    )
                    if request["status"] == "Open":
                        if st.button(
                            "Resolve",
                            key=f"resolve_{request['id']}",
                        ):
                            request["status"] = "Resolved"
                            st.rerun()
with tab3:
    st.header("ℹ️ About MicroHelp AI")
    st.write(
        """
        **MicroHelp AI** is a smart assistance platform
        designed to understand small everyday problems
        and identify the skill required to solve them.
        The platform can:
        - 📝 Accept a user's problem
        - 🤖 Analyze the problem
        - 🧠 Identify the required skill
        - 👨‍💻 Suggest the right type of helper
        - 📨 Create a help request
        - 📋 Display active requests
        - ✅ Track resolved requests
        """
    )
    st.divider()
    st.subheader("🎯 Project Goal")
    st.write(
        "Connect people who need quick assistance with "
        "people who have the appropriate skills."
    )
    st.subheader("🔮 Future Enhancements")
    st.write(
        """
        - AI-powered natural language understanding
        - User registration and login
        - Helper profiles
        - Skill-based matching
        - Location-based matching
        - Real-time chat
        - Ratings and reviews
        - Database integration
        - Google Gemini/OpenAI integration
        - Admin dashboard
        """
    )
st.divider()
st.caption(
    "MicroHelp AI • AI-powered everyday assistance platform"
)