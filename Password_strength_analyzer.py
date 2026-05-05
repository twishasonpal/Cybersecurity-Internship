import re

def check_password_strength(password):
    score = 0
    feedback = []

    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")

    # Uppercase check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter")

    # Lowercase check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter")

    # Digit check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number")

    # Special character check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add at least one special character")

    # Strength result
    if score == 5:
        strength = "Very Strong 🔥"
    elif score >= 3:
        strength = "Moderate ⚠️"
    else:
        strength = "Weak ❌"

    return strength, feedback


# Main program
password = input("Enter your password: ")

strength, feedback = check_password_strength(password)

print("\nPassword Strength:", strength)

if feedback:
    print("Suggestions:")
    for tip in feedback:
        print("-", tip)
else:
    print("Great! Your password is secure ✅")
