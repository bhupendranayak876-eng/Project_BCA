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
    common_patterns = ["1234", "password", "admin", "qwerty", "abc123"]()_
