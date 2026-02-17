import streamlit as st
import re
import secrets
import string
import math

# -----------------------------
# Secure Password Generator
# -----------------------------
def generate_secure_password(length, use_symbols):
    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += string.punctuation

    return ''.join(secrets.choice(characters) for _ in range(length))


# -----------------------------
# Password Strength Check
# -----------------------------
def check_password(password):
    score = 0
    suggestions = []

    # Length
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    # Numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Include numbers.")

    # Symbols
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Include special characters.")

    # Common Patterns
    common_patterns = ["1234", "password", "admin", "qwerty", "abc123"]
    for pattern in common_patterns:
        if pattern in password.lower():
            score -= 1
            suggestions.append("Avoid common patterns.")
            break

    return max(score, 0), suggestions


# -----------------------------
# Strength Level
# -----------------------------
def strength_level(score):
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"


# -----------------------------
# Entropy Calculation
# -----------------------------
def calculate_entropy(password):
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        pool += 32

    if pool == 0:
        return 0

    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)


# -----------------------------
# Modern UI Styling
# -----------------------------
st.set_page_config(page_title="Secure Password Tool", page_icon="🔐")

st.markdown("""
<style>
.big-title {
    font-size:30px !important;
    font-weight:700;
    color:#4CAF50;
}
.section {
    background-color:#f5f5f5;
    padding:20px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🔐 Advanced Secure Password Analyzer</p>', unsafe_allow_html=True)

st.write("A cybersecurity tool to analyze and generate strong passwords.")

# -----------------------------
# Generator Section
# -----------------------------
st.markdown("## 🔑 Generate Secure Password")

length = st.slider("Select Password Length", 8, 32, 12)
use_symbols = st.checkbox("Include Special Characters")

if st.button("Generate Secure Password"):
    secure_password = generate_secure_password(length, use_symbols)
    st.success("Generated Password:")
    st.code(secure_password)

st.divider()

# -----------------------------
# Analyzer Section
# -----------------------------
st.markdown("## 📊 Analyze Password")

password = st.text_input("Enter Password:", type="password")

if password:
    score, suggestions = check_password(password)
    level = strength_level(score)
    entropy = calculate_entropy(password)

    # Strength Display
    if level == "Weak":
        st.error(f"Strength: {level}")
    elif level == "Medium":
        st.warning(f"Strength: {level}")
    else:
        st.success(f"Strength: {level}")

    # Progress Bar
    st.progress(score / 5)

    st.write(f"Score: {score} / 5")
    st.write(f"Entropy: {entropy} bits")

    if entropy < 40:
        st.error("Low entropy — vulnerable to brute-force attacks.")
    elif entropy < 60:
        st.warning("Moderate entropy — can be improved.")
    else:
        st.success("High entropy — strong password.")

    if suggestions:
        st.subheader("Suggestions:")
        for s in suggestions:
            st.write(f"- {s}")
    else:
        st.success("Excellent! Your password meets strong security standards.")
