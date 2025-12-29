import streamlit as st
from openai import OpenAI

# ---------------- OPENAI CLIENT ---------------- #
client = OpenAI()

# ---------------- STREAMLIT CONFIG ---------------- #
st.set_page_config(
    page_title="Personal LinkedIn Manager AI",
    page_icon="💼",
    layout="centered"
)

# ---------------- SESSION STATE INIT ---------------- #
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ---------------- MASTER PROMPT ---------------- #
LINKEDIN_MANAGER_PROMPT = """
You are my personal LinkedIn Growth Manager AI.

Your role:
- Act like a senior LinkedIn strategist with deep understanding of recruiter psychology.
- Optimize my LinkedIn presence to attract internships, recruiters, and freelance clients.
- Think long-term brand building, not short-term likes.

About me:
- Role target: Applied AI Engineer (LLMs & Prompt Engineering)
- Strengths: Prompt engineering, building & deploying AI tools
- Goal: Get noticed by recruiters and founders
- Tone: Professional, builder mindset, confident but not arrogant
- Avoid words: student, beginner, learning

Rules:
- Clear hook in first 2 lines
- Short paragraphs
- Simple language
- Soft CTA

Output Format:

POST_DECISION:
Yes / No

POST_TYPE:
<type>

POST_CONTENT:
<full LinkedIn post>

BEST_TIME:
<time in IST>

HASHTAGS:
#tag1 #tag2 #tag3
"""

def generate_linkedin_content(user_request: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": LINKEDIN_MANAGER_PROMPT},
            {"role": "user", "content": user_request}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content


# ---------------- STYLING ---------------- #
st.markdown("""
<style>
.stApp { background-color: #0e1117; color: #e6e6e6; }
h1, h2, h3 { color: white; font-weight: 700; }
.card {
    background-color: #ffffff;
    color: #000000;
    padding: 20px;
    border-radius: 12px;
    font-size: 16px;
    line-height: 1.6;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.35);
}
.badge {
    display: inline-block;
    background-color: #2563eb;
    color: white;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.markdown("<h1 style='text-align:center;'>💼 Personal LinkedIn Manager AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>Your AI assistant for LinkedIn growth, content & consistency</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- OPTIONS ---------------- #
option = st.selectbox(
    "What do you want to do?",
    [
        "Write today’s LinkedIn post",
        "Plan my LinkedIn content for 7 days",
        "Write a post about something I built",
        "Optimize an existing LinkedIn post"
    ]
)

# ---------------- CONDITIONAL INPUT ---------------- #
if option == "Write a post about something I built":
    st.text_area(
        "Describe what you built:",
        key="user_input",
        placeholder="e.g. I built a Prompt Debugger AI using Streamlit and OpenAI APIs",
        height=120
    )

elif option == "Optimize an existing LinkedIn post":
    st.text_area(
        "Paste your LinkedIn post:",
        key="user_input",
        height=150
    )

# ---------------- GENERATE ---------------- #
if st.button("✨ Generate"):

    # Validation
    if option in [
        "Write a post about something I built",
        "Optimize an existing LinkedIn post"
    ] and not st.session_state.user_input.strip():
        st.warning("Please enter the required text.")
        st.stop()

    with st.spinner("Your LinkedIn Manager AI is thinking..."):

        if option == "Write today’s LinkedIn post":
            raw_output = generate_linkedin_content("Write today’s LinkedIn post")

        elif option == "Plan my LinkedIn content for 7 days":
            raw_output = generate_linkedin_content(
                "Create a clear 7-day LinkedIn content plan with topics and post types."
            )

        elif option == "Write a post about something I built":
            raw_output = generate_linkedin_content(
                f"I built this today: {st.session_state.user_input}. Write a LinkedIn post about it."
            )

        elif option == "Optimize an existing LinkedIn post":
            raw_output = generate_linkedin_content(
                f"Optimize this LinkedIn post for better reach and recruiter appeal:\n{st.session_state.user_input}"
            )

    # ---------------- PARSE OUTPUT ---------------- #
    try:
        decision = raw_output.split("POST_DECISION:")[1].split("POST_TYPE:")[0].strip()
        post_type = raw_output.split("POST_TYPE:")[1].split("POST_CONTENT:")[0].strip()
        post_content = raw_output.split("POST_CONTENT:")[1].split("BEST_TIME:")[0].strip()
        best_time = raw_output.split("BEST_TIME:")[1].split("HASHTAGS:")[0].strip()
        hashtags = raw_output.split("HASHTAGS:")[1].strip()
    except:
        st.error("Unexpected response format. Try again.")
        st.stop()

    st.markdown("---")

    st.markdown("## 📌 Decision to Post Today")
    st.markdown(f"<span class='badge'>{decision}</span>", unsafe_allow_html=True)

    st.markdown("## 📝 Post Type")
    st.markdown(f"<span class='badge'>{post_type}</span>", unsafe_allow_html=True)

    st.markdown("## ✍️ LinkedIn Post (Ready to Publish)")
    st.markdown(f"<div class='card'>{post_content}</div>", unsafe_allow_html=True)

    st.markdown("## ⏰ Best Time to Post")
    st.markdown(f"<span class='badge'>{best_time}</span>", unsafe_allow_html=True)

    st.markdown("## 🔖 Hashtags")
    st.markdown(f"<div class='card'>{hashtags}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Built by an Applied AI Engineer | Personal LinkedIn Manager AI")
