

import streamlit as st\
import re\
\
# ------------------------------\
# Password Strength Function\
# ------------------------------\
def check_password_strength(password):\
    score = 0\
    suggestions = []\
\
    if len(password) >= 8:\
        score += 1\
    else:\
        suggestions.append("Make password at least 8 characters long.")\
\
    if re.search(r"[A-Z]", password):\
        score += 1\
    else:\
        suggestions.append("Add at least one uppercase letter.")\
\
    if re.search(r"[a-z]", password):\
        score += 1\
    else:\
        suggestions.append("Add at least one lowercase letter.")\
\
    if re.search(r"[0-9]", password):\
        score += 1\
    else:\
        suggestions.append("Include at least one number.")\
\
    if re.search(r"[!@#$%^&*(),.?\\":\{\}|<>]", password):\
        score += 1\
    else:\
        suggestions.append("Add at least one special character.")\
\
    weak_passwords = ["password", "123456", "qwerty", "admin"]\
    if password.lower() in weak_passwords:\
        score = 0\
        suggestions.append("This is a very common password. Choose something unique.")\
\
    return score, suggestions\
\
\
def get_strength_level(score):\
    if score <= 2:\
        return "Weak"\
    elif score == 3 or score == 4:\
        return "Medium"\
    else:\
        return "Strong"\
\
\
# ------------------------------\
# Streamlit UI\
# ------------------------------\
st.set_page_config(page_title="Password Strength Analyzer", page_icon="\uc0\u55357 \u56592 ")\
\
st.title("\uc0\u55357 \u56592  Password Strength Analyzer")\
st.write("Check how strong your password is!")\
\
password = st.text_input("Enter your password:", type="password")\
\
if password:\
    score, suggestions = check_password_strength(password)\
    strength = get_strength_level(score)\
\
    st.subheader("Result:")\
\
    if strength == "Weak":\
        st.error(f"Strength: \{strength\}")\
    elif strength == "Medium":\
        st.warning(f"Strength: \{strength\}")\
    else:\
        st.success(f"Strength: \{strength\}")\
\
    st.write(f"Score: \{score\} / 5")\
\
    if suggestions:\
        st.subheader("Suggestions to Improve:")\
        for s in suggestions:\
            st.write(f"- \{s\}")\
    else:\
        st.success("Excellent! Your password is strong.")\
}
