import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import auth

st.set_page_config(page_title="Python Quiz", layout="centered")

st.title("🧠 Python Fundamentals Quiz")
st.write("Test your understanding of Python fundamentals and functions.")

RESULTS_FILE = Path("quiz_results.json")


def load_results():
    if RESULTS_FILE.exists():
        try:
            with open(RESULTS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []  # empty file -> return empty list
                return json.loads(content)
        except json.JSONDecodeError:
            # Malformed file -> reset
            return []
    return []


def save_result(username, score, total):
    results = load_results()

    # Count how many tests this user has already taken
    user_tests = [r for r in results if r["username"] == username]
    test_number = len(user_tests) + 1

    result_entry = {
        "username": username,
        "test_number": test_number,
        "score": score,
        "total": total,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    results.append(result_entry)

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)


# ----------------------------
# Quiz Data
# ----------------------------
quiz = [
    {
        "question": "What is the output?\n\nx = 10\ny = '10'\nprint(x + int(y))",
        "options": ["1010", "20", "Error", "10 10"],
        "answer": "20"
    },
    {
        "question": "Which of the following is a mutable data type?",
        "options": ["tuple", "int", "list", "str"],
        "answer": "list"
    },
    {
        "question": "What is the data type of input() in Python?",
        "options": ["int", "float", "str", "depends on input"],
        "answer": "str"
    },
    {
        "question": "What will be printed?\n\ndef greet(name='Guest'):\n    print('Hello', name)\n\ngreet()",
        "options": ["Hello", "Hello None", "Hello Guest", "Error"],
        "answer": "Hello Guest"
    },
    {
        "question": "Which rule is correct for default arguments?",
        "options": [
            "Default arguments must come first",
            "Default arguments must come after positional arguments",
            "Default arguments cannot be strings",
            "Python does not support default arguments"
        ],
        "answer": "Default arguments must come after positional arguments"
    },
    {
        "question": "What is the type of *args?",
        "options": ["list", "tuple", "set", "dict"],
        "answer": "tuple"
    },
    {
        "question": "What will **kwargs store?",
        "options": ["list", "tuple", "set", "dictionary"],
        "answer": "dictionary"
    },
    {
        "question": "What will be printed?\n\nstudent(age=25, name='Amit')",
        "options": ["25 Amit", "Amit 25", "Error", "Depends on order"],
        "answer": "Amit 25"
    }
]



if not auth.is_authenticated():
    st.warning("🔒 Please login to access the quiz.")
    st.stop()



# ----------------------------
# Store Answers
# ----------------------------
if "answers" not in st.session_state:
    st.session_state.answers = {}

# ----------------------------
# Quiz UI
# ----------------------------
for idx, q in enumerate(quiz):
    st.subheader(f"Q{idx + 1}.")
    st.code(q["question"], language="python")

    options = ["-- Select an option --"] + q["options"]

    selected = st.radio(
    "Choose an option:",
    options,
    key=f"q_{idx}"
    )

    st.session_state.answers[idx] = selected
    st.divider()

# ----------------------------
# Submit Button
# ----------------------------
# if st.button("📊 Submit Quiz"):
#     score = 0

#     st.subheader("📊 Quiz Results")
#     st.divider()

#     for idx, q in enumerate(quiz):
#         user_ans = st.session_state.answers.get(idx)
#         correct_ans = q["answer"]

#         if user_ans == correct_ans:
#             score += 1
#             st.success(f"Q{idx + 1}: Correct ✅")
#         else:
#             st.error(f"Q{idx + 1}: Incorrect ❌")
#             st.write(f"👉 Correct answer: **{correct_ans}**")

#     st.divider()
#     st.metric("Your Score", f"{score} / {len(quiz)}")

#     if score == len(quiz):
#         st.balloons()
#         st.success("🎉 Excellent! Perfect score!")
#     elif score >= len(quiz) * 0.6:
#         st.info("👍 Good job! Keep practicing.")
#     else:
#         st.warning("📘 Revise concepts and try again.")


if st.button("📊 Submit Quiz"):
    if None in st.session_state.answers.values():
        st.warning("⚠️ Please answer all questions before submitting.")
        st.stop()

    score = 0
    total_questions = len(quiz)

    for idx, q in enumerate(quiz):
        user_ans = st.session_state.answers.get(idx)
        correct_ans = q["answer"]

        if user_ans == correct_ans:
            score += 1
            st.success(f"Q{idx + 1}: Correct ✅")
        else:
            st.error(f"Q{idx + 1}: Incorrect ❌")
            st.write(f"👉 Correct answer: **{correct_ans}**")

    # 🔐 Get logged-in user
    user = auth.get_current_user()
    username = user["name"]

    # 💾 Save result
    save_result(username, score, total_questions)

    # 📊 Show results
    st.subheader("📊 Quiz Results")
    st.metric("Score", f"{score} / {total_questions}")

    if score == total_questions:
        st.balloons()
        st.success("🎉 Perfect score!")
    elif score >= total_questions * 0.6:
        st.info("👍 Good job!")
    else:
        st.warning("📘 Needs more practice")

