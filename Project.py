import streamlit as st
import re
import secrets
import string
import math
from fpdf import FPDF
import tempfile

# -----------------------------
# Secure Password Generator
# -----------------------------
def generate_secure_password(length, use_symbols):
    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

# -----------------------------
# Strength Check
# -----------------------------
def check_password(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Include numbers.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Include special characters.")

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
# PDF Report Generator
# -----------------------------
def generate_pdf(password, level, score, entropy, suggestions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Password Security Report", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Password Entered: {password}", ln=True)
    pdf.cell(200, 10, txt=f"Strength Level: {level}", ln=True)
    pdf.cell(200, 10, txt=f"Score: {score} / 5", ln=True)
    pdf.cell(200, 10, txt=f"Entropy: {entropy} bits", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Suggestions:", ln=True)

    if suggestions:
        for s in suggestions:
            pdf.multi_cell(0, 10, txt=f"- {s}")
    else:
        pdf.multi_cell(0, 10, txt="Password meets strong security standards.")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Secure Password Tool", page_icon="🔐")
st.title("🔐 Secure Password Analyzer & Generator")

# Generator Section
st.subheader("🔑 Generate Secure Password")
length = st.slider("Select Password Length", 8, 32, 12)
use_symbols = st.checkbox("Include Special Characters")

if st.button("Generate Password"):
    st.code(generate_secure_password(length, use_symbols))

st.divider()

# Analyzer Section
st.subheader("📊 Analyze Password")
password = st.text_input("Enter Password:", type="password")

if password:
    score, suggestions = check_password(password)
    level = strength_level(score)
    entropy = calculate_entropy(password)

    if level == "Weak":
        st.error(f"Strength: {level}")
    elif level == "Medium":
        st.warning(f"Strength: {level}")
    else:
        st.success(f"Strength: {level}")

    st.progress(score / 5)
    st.write(f"Score: {score} / 5")
    st.write(f"Entropy: {entropy} bits")

    if suggestions:
        for s in suggestions:
            st.write(f"- {s}")
    else:
        st.success("Strong password!")

    # PDF Download Button
    pdf_file = generate_pdf(password, level, score, entropy, suggestions)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download Security Report (PDF)",
            data=f,
            file_name="Password_Security_Report.pdf",
            mime="application/pdf"
        )
