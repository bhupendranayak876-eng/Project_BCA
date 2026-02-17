import streamlit as st
import re
import random
import string

# ------------------------------
# Password Generator Function
# ------------------------------
def generate_password(length, use_symbols):
    characters = string.ascii_letters + string.digits
    if use_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


# ------------------------------
# Password Strength Checker
# ------------------------------
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
        suggestions.append("Add uppercase letters (A-Z).")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters (a-z).")

    # Numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Include numbers (0-9).")

    # Symbols
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Include special symbols (!@#$ etc).")

    # Common Patterns
    common_patterns = ["1234", "password", "admin", "qwerty", "abc123"]

    for pattern in common_patterns:
        if pattern in password.lower():
            score -= 1
            suggestions.append("Avoid common patterns like '1234', 'password', etc.")
            break

    return score, suggestions


# ------------------------------
# Strength Level
# ------------------------------
def strength_level(score):
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"


# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Password Strength Analyzer", page_icon="🔐")

st.title("🔐 Password Strength Analyzer & Generator")
st.write("Analyze and generate secure passwords.")

# ------------------------------
# Generator Section
# ------------------------------
st.subheader("🔑 Generate Strong Password")

length = st.slider("Select password length", 8, 32, 12)
use_symbols = st.checkbox("Include Special Characters")

if st.button("Generate Password"):
    generated_password = generate_password(length, use_symbols)
    st.success("Generated Password:")
    st.code(generated_password)

st.divider()

# ------------------------------
# Analyzer Section
# ------------------------------
st.subheader("📊 Analyze Your Password")

password = st.text_input("Enter your password:", type="password")

if password:
    score, suggestions = check_password(password)
    level = strength_level(score)

    if level == "Weak":
        st.error(f"Strength: {level}")
    elif level == "Medium":
        st.warning(f"Strength: {level}")
    else:
        st.success(f"Strength: {level}")

    st.write(f"Score: {score} / 5")

    if suggestions:
        st.subheader("⚠ Suggestions to Improve:")
        for s in suggestions:
            st.write(f"- {s}")
    else:
        st.success("Excellent! Your password is strong.")
