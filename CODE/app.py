import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Sample data
student_data = pd.DataFrame({
    "student_name": [f"Student_{i}" for i in range(1, 31)],
    "department": ["BA"] * 10 + ["BB"] * 10 + ["BC"] * 10,
    "student_id": [f"01523300{i:02d}" for i in range(1, 31)],
    "cgpa": [round(2.5 + (i % 5) * 0.2, 2) for i in range(1, 31)]
})

attendance_data = pd.DataFrame({
    "student_id": [f"01523300{i:02d}" for i in range(1, 31)],
    "attendance_percentage": [round(80 + (i % 5) * 3, 2) for i in range(1, 31)],
    "punctuality_percentage": [round(85 + (i % 4) * 2, 2) for i in range(1, 31)]
})
ct_marks_data = pd.DataFrame({
    "student_id": [f"01523300{i:02d}" for i in range(1, 31)],
    "ct1_marks": [round(50 + (i % 5) * 5, 2) for i in range(1, 31)],
    "ct2_marks": [round(55 + (i % 6) * 4, 2) for i in range(1, 31)],
    "ct3_marks": [round(60 + (i % 4) * 3, 2) for i in range(1, 31)]
})
# Sample data for 24 daily classes
punctuality_data = pd.DataFrame({
    "class": [f"Class {i}" for i in range(1, 25)],
    "in_time": [(datetime.strptime("08:00", "%H:%M") + timedelta(minutes=random.randint(-10, 10))).strftime("%H:%M") for _ in range(24)],
    "out_time": [(datetime.strptime("10:00", "%H:%M") + timedelta(minutes=random.randint(-10, 10))).strftime("%H:%M") for _ in range(24)]
})
# Convert time to datetime objects
punctuality_data["in_time"] = pd.to_datetime(punctuality_data["in_time"], format="%H:%M")
punctuality_data["out_time"] = pd.to_datetime(punctuality_data["out_time"], format="%H:%M")

# Calculate duration in minutes
punctuality_data["duration"] = (punctuality_data["out_time"] - punctuality_data["in_time"]).dt.total_seconds() / 60

# Calculate punctuality percentage (max duration per class = 120 minutes)
punctuality_data["punctuality_percentage"] = [(d / 120) * 100 + random.uniform(-10, 10) for d in punctuality_data["duration"]]

# Ensure values are within bounds (0 to 100)
punctuality_data["punctuality_percentage"] = punctuality_data["punctuality_percentage"].clip(0, 100)

# Streamlit page configuration
st.set_page_config(page_title="BioMetric Attendance System", layout="wide")

# Generate default student data with scores
n_student_data = pd.DataFrame({
    "Student Name": [f"Student_{i}" for i in range(1, 31)],
    "Student ID": [f"01523300{i:02d}" for i in range(1, 31)],
    "Punctuality": [2.5] * 22 + [2.0] * 5 + [1.5] * 3,
    "Attendance": [2.5] * 22 + [2.0] * 5 + [1.5] * 3
})

# Custom styling
st.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            background-color: #2E4053;
            color: white;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            background-color: #1ABC9C;
            color: white;
        }
        h1 {
            color: #2C3E50;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Login Page
st.sidebar.title("Login")
role = st.sidebar.selectbox("Login as", ["Admin", "Student", "Teacher"])
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

# Login Credentials
admin_credentials = {"admin123": "12345"}
student_credentials = {f"01523300{i:02d}": "12345" for i in range(1, 31)}
teacher_credentials = {"teacher": "12345"}

# Authentication
if login_button:
    if role == "Admin" and username in admin_credentials and password == admin_credentials[username]:
        st.session_state['authenticated'] = True
        st.session_state['role'] = "Admin"
    elif role == "Student" and username in student_credentials and password == student_credentials[username]:
        st.session_state['authenticated'] = True
        st.session_state['role'] = "Student"
        st.session_state['student_id'] = username
    elif role == "Teacher" and username in teacher_credentials and password == teacher_credentials[username]:
        st.session_state['authenticated'] = True
        st.session_state['role'] = "Teacher"
    else:
        st.sidebar.error("Invalid credentials. Please try again.")

# Logout option
if st.sidebar.button("Log Out"):
    st.session_state.clear()
    st.sidebar.success("Logged out successfully!")

# Dashboard Navigation
if st.session_state.get('authenticated', False):

    if st.session_state['role'] == "Admin":
        st.sidebar.title("Admin Dashboard")
        admin_option = st.sidebar.radio("Choose an option",
                                        ["Upload Student Data", "Add Student", "Search Student"])

        st.title("Admin Dashboard")

        if admin_option == "Upload Student Data":
            st.header("Upload Student Data CSV")
            uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
            if uploaded_file:
                st.session_state['student_data'] = pd.read_csv(uploaded_file)
                st.dataframe(st.session_state['student_data'])

        elif admin_option == "Add Student":
            st.subheader("Add New Student")
            name = st.text_input("Student Name")
            dept = st.selectbox("Department", ["BA", "BB", "BC"])
            student_id = st.text_input("Student ID")
            cgpa = st.number_input("Current CGPA", min_value=0.0, max_value=4.0, step=0.01)

            if "student_data" not in st.session_state:
                st.session_state.student_data = student_data

            if st.button("Add Student"):
                new_student = pd.DataFrame({
                    "student_name": [name],
                    "department": [dept],
                    "student_id": [student_id],
                    "cgpa": [cgpa]
                })
                st.session_state.student_data = pd.concat([st.session_state.student_data, new_student], ignore_index=True)
                st.success("Student added successfully!")

        elif admin_option == "Search Student":
            st.subheader("Search Student by ID")
            search_id = st.text_input("Enter Student ID")
            if st.button("Search"):
                result = student_data[student_data["student_id"] == search_id]
                if not result.empty:
                    st.write(result)
                else:
                    st.warning("No student found with this ID.")

    elif st.session_state['role'] == "Student":
        st.sidebar.title("Student Dashboard")
        course_selection = st.sidebar.selectbox("Course Selection", ["Course 1", "Course 2", "Course 3"])
        student_option = st.sidebar.radio("Performance", ["CGPA Chart", "Attendance", "Punctuality","Class Test Marks"])

        st.title("Student Dashboard")

        if student_option == "CGPA Chart":
            st.subheader("CGPA Progression")
            fig = px.line(x=["Trimester 1", "Trimester 2", "Trimester 3" ,"Trimester 4" ],
                          y=[2.7, 3.00, 3.6 , 3.4],
                          markers=True, title="CGPA Trend")
            st.plotly_chart(fig)

        elif student_option == "Attendance":
            st.subheader("Attendance Overview")
            att_data = attendance_data[attendance_data["student_id"] == st.session_state['student_id']]
            fig = px.pie(names=["Missed Classes", "Attended Classes"],
                         values=[100 - att_data["attendance_percentage"].values[0],
                                 att_data["attendance_percentage"].values[0]],
                         title="Attendance Overview")
            st.plotly_chart(fig)

        elif student_option == "Punctuality":
            st.subheader("Punctuality Overview (Based on In and Out Times)")
            fig = px.bar(punctuality_data, x="class", y="punctuality_percentage",
             title="Punctuality Records (Daily 24 Classes with Fluctuations)",
             labels={'x': 'Class', 'y': 'Punctuality (%)'},
             color="punctuality_percentage",
             color_continuous_scale="Turbo")
            st.plotly_chart(fig)
           
        elif student_option == "Class Test Marks":
            st.subheader("Class Test Performance")
            class_test_marks = {
                "Class Test 1": 18,
                "Class Test 2": 10,
                "Class Test 3": 14
            }
            fig = px.bar(x=list(class_test_marks.keys()), y=list(class_test_marks.values()),
                         labels={"x": "Class Tests", "y": "Marks"},
                         title="Class Test Performance Overview")
            st.plotly_chart(fig)

    elif st.session_state['role'] == "Teacher":
        st.sidebar.title("Teacher Dashboard")
        section = st.sidebar.selectbox("Select Section", ["BA", "BB", "BC"])
        teacher_option = st.sidebar.radio("Choose an option", [ "Upload Attendance","Upload Marks", "View Attendance","Generate Attendence Report"])

        st.title("Teacher Dashboard")

        if teacher_option == "View Attendance":
            st.subheader(f"Attendance Records for Section {section}")
            section_data = student_data[student_data["department"] == section]
            merged_data = pd.merge(section_data, attendance_data, on="student_id")
            fig = px.bar(merged_data, x="student_name", y=["cgpa", "attendance_percentage", "punctuality_percentage"],
                         barmode="group", title="Student Performance Overview")
            st.plotly_chart(fig)

        elif teacher_option == "Upload Marks":
            st.subheader("Upload Class Test Marks CSV")

            uploaded_file = st.file_uploader("Choose a Marks CSV file", type=["csv"])

            if uploaded_file:
                # Read the uploaded file
                df = pd.read_csv(uploaded_file)

                # Check if required columns exist
                if "student_id" in df.columns and "marks" in df.columns:
                    st.success("Marks file uploaded successfully!")
                   
                    # Display uploaded data
                    st.write("Uploaded Class Test Marks:")
                    st.dataframe(df)

                    # Generate a bar chart for marks distribution
                    st.subheader("Class Test Marks Distribution")
                    fig = px.bar(df, x="student_id", y="marks", title="Class Test Marks", labels={"student_id": "Student ID", "marks": "Marks"})
                    st.plotly_chart(fig)

                    # Generate a pie chart for grade distribution
                    st.subheader("Marks Percentage Distribution")
                    df['grade_category'] = pd.cut(df['marks'], bins=[0, 50, 70, 90, 100],
                                                labels=["Below Average", "Average", "Good", "Excellent"])
                    grade_counts = df['grade_category'].value_counts()
                    pie_chart = px.pie(names=grade_counts.index, values=grade_counts.values, title="Grade Distribution")
                    st.plotly_chart(pie_chart)
                   
                else:
                    st.error("Uploaded CSV must contain 'student_id' and 'marks' columns.")

        elif teacher_option == "Upload Attendance":
            st.subheader("Upload Attendance CSV")
            uploaded_file = st.file_uploader("Choose an Attendance CSV file", type=["csv"])
            if uploaded_file:
                st.session_state['attendence_data'] = pd.read_csv(uploaded_file)
                st.dataframe(st.session_state['attendence_data'])
                st.success("Attendance file uploaded successfully!")
               
        elif teacher_option == "Generate Attendence Report":
            # Calculate total marks
            n_student_data["Total Marks"] = n_student_data["Punctuality"] + n_student_data["Attendance"]
            st.title("Student Performance Data")
            st.subheader("Punctuality and Attendance Overview")
            st.dataframe(n_student_data)
           
           
else:
    st.title("Welcome to the BioMetric Attendance System")
    st.write("Please login to continue.")