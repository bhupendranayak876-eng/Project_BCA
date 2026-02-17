import streamlit as st
import re
import random
import string

# ------------------------------
# Generate Strong Password Example
# ------------------------------
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


# ------------------------------
# Password Strength Checker
# ------------------------------
def check_password(password):
    score = 0
    suggestions = []

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    # Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters (A-Z).")

    # Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters (a-z).")

    # Number Check
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Include numbers (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Include special symbols (!@#$ etc).")

    # Common Patterns Detection
    common_patterns = [
        "1234", "password", "admin", "qwerty", "abc123"
    ]

    for pattern in common_patterns:
        if pattern in password.lower():
            suggestions.append("Avoid common patterns like '1234', 'password', etc.")
            score -= 1
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

st.title("🔐 Password Strength Analyzer")
st.write("Check how secure your password is.")

password = st.text_input("Enter your password:", type="password")

if password:
    score, suggestions = check_password(password)
    level = strength_level(score)

    st.subheader("📊 Analysis Result")

    # Display Strength
    if level == "Weak":
        st.error(f"Strength: {level}")
    elif level == "Medium":
        st.warning(f"Strength: {level}")
    else:
        st.success(f"Strength: {level}")

    st.write(f"Score: {score} / 5")

    # Suggestions
    if suggestions:
        st.subheader("⚠ Suggestions to Improve:")
        for s in suggestions:
            st.write(f"- {s}")

        # Suggest Better Password Example
        st.subheader("💡 Suggested Strong Password Example:")
        st.code(generate_strong_password())
    else:
        st.success("Excellent! Your password meets strong security standards.")
