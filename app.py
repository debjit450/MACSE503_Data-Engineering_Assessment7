# MACSE503 - Data Engineering | Assessment 7 | Question 1

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# ---------- Title ----------
st.title("Student Performance Dashboard")
st.write("Analysis of student marks and attendance.")

# ---------- Sidebar (interactive controls) ----------
st.sidebar.header("Dataset and Filters")

# the default dataset is students.csv, but the user can also upload another csv
uploaded_file = st.sidebar.file_uploader("Upload a student CSV (optional)", type="csv")

required_cols = ["student_id", "student_name", "math_score", "science_score",
                 "english_score", "attendance_percentage"]

# ---------- Load the dataset ----------
df = pd.read_csv("students.csv")

if uploaded_file is not None:
    new_df = pd.read_csv(uploaded_file)
    if all(col in new_df.columns for col in required_cols):
        df = new_df
    else:
        st.sidebar.error("Uploaded file must have these columns: " + ", ".join(required_cols))

min_att = st.sidebar.slider(
    "Minimum attendance percentage",
    min_value=int(df["attendance_percentage"].min()),
    max_value=int(df["attendance_percentage"].max()),
    value=int(df["attendance_percentage"].min()),
)
show_data = st.sidebar.checkbox("Show dataset", value=True)

# filter the data using the slider value
filtered_df = df[df["attendance_percentage"] >= min_att]

if filtered_df.empty:
    st.warning("No students found for the selected attendance.")
    st.stop()

st.write(f"Students shown: {len(filtered_df)} out of {len(df)}")

# ---------- Display the dataset ----------
if show_data:
    st.subheader("Student Dataset")
    st.dataframe(filtered_df)

# ---------- Math score statistics ----------
st.subheader("Math Score Statistics")

math = filtered_df["math_score"]
mean_val = math.mean()
median_val = math.median()
mode_list = math.mode().tolist()   # can have more than one mode
std_val = math.std()

# show all modes if there is a tie
mode_text = ", ".join(str(m) for m in mode_list)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Mean", round(mean_val, 2))
col2.metric("Median", median_val)
col3.metric("Mode", mode_text)
col4.metric("Standard Deviation", round(std_val, 2))
st.caption("Standard deviation is the sample standard deviation (divided by n - 1).")

# ---------- Bar chart: average score of each subject ----------
st.subheader("Average Score for Each Subject")

avg_scores = filtered_df[["math_score", "science_score", "english_score"]].mean()
subjects = ["Math", "Science", "English"]

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(subjects, avg_scores.values, color=["steelblue", "seagreen", "orange"])
ax.set_title("Average Score for Each Subject")
ax.set_xlabel("Subject")
ax.set_ylabel("Average Score")
ax.set_ylim(0, 100)

# write the value on top of each bar
for i, v in enumerate(avg_scores.values):
    ax.text(i, v + 1, round(v, 1), ha="center")

st.pyplot(fig)

# ---------- Insights ----------
st.subheader("Insights")

best_subject = subjects[avg_scores.values.argmax()]
weak_subject = subjects[avg_scores.values.argmin()]
top_student = filtered_df.loc[filtered_df["math_score"].idxmax()]

st.write(f"- Highest average subject: {best_subject} ({avg_scores.max():.2f})")
st.write(f"- Lowest average subject: {weak_subject} ({avg_scores.min():.2f})")
st.write(f"- Top math scorer: {top_student['student_name']} with {top_student['math_score']} marks")
st.write(f"- Students scoring below 60 in math: {int((math < 60).sum())}")
