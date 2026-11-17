import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Student Record Management",
    page_icon="🎓",
    layout="wide"
)

# File to store student records
FILE = "students.csv"

# Load student data
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=[
        "Roll No", "Name", "Age", "Course", "Email"
    ])

# Save data
def save_data():
    df.to_csv(FILE, index=False)

st.title("🎓 Student Record Management System")
st.write("Manage student records using CRUD operations.")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("➕ Add New Student")

    with st.form("add_form"):
        roll = st.number_input("Roll Number", min_value=1, step=1)
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        course = st.text_input("Course")
        email = st.text_input("Email")

        submit = st.form_submit_button("Add Student")

        if submit:
            if not name or not course or not email:
                st.error("Please fill all fields.")
            elif roll in df["Roll No"].values:
                st.error("Roll number already exists!")
            else:
                new_student = pd.DataFrame([{
                    "Roll No": roll,
                    "Name": name,
                    "Age": age,
                    "Course": course,
                    "Email": email
                }])

                df = pd.concat(
                    [df, new_student],
                    ignore_index=True
                )

                save_data()
                st.success("Student added successfully!")

# READ
elif menu == "View Students":
    st.subheader("📋 All Student Records")

    if df.empty:
        st.info("No student records found.")
    else:
        st.dataframe(df, use_container_width=True)
        st.write("Total Students:", len(df))

# UPDATE
elif menu == "Update Student":
    st.subheader("✏️ Update Student Details")

    if df.empty:
        st.info("No records available to update.")
    else:
        roll = st.selectbox(
            "Select Roll Number",
            df["Roll No"].tolist()
        )

        student = df[df["Roll No"] == roll].iloc[0]

        with st.form("update_form"):
            name = st.text_input("Name", value=str(student["Name"]))
            age = st.number_input(
                "Age",
                min_value=1,
                max_value=100,
                value=int(student["Age"])
            )
            course = st.text_input(
                "Course", value=str(student["Course"])
            )
            email = st.text_input(
                "Email", value=str(student["Email"])
            )

            update = st.form_submit_button("Update Student")

            if update:
                if not name or not course or not email:
                    st.error("Please fill all fields.")
                else:
                    df.loc[df["Roll No"] == roll, [
                        "Name", "Age", "Course", "Email"
                    ]] = [name, age, course, email]

                    save_data()
                    st.success("Student updated successfully!")

# DELETE
elif menu == "Delete Student":
    st.subheader("🗑️ Delete Student Record")

    if df.empty:
        st.info("No records available to delete.")
    else:
        roll = st.selectbox(
            "Select Roll Number to Delete",
            df["Roll No"].tolist()
        )

        st.write(
            df[df["Roll No"] == roll].to_dict(orient="records")[0]
        )

        if st.button("Delete Student"):
            df = df[df["Roll No"] != roll]
            save_data()
            st.success("Student deleted successfully!")

st.sidebar.markdown("---")
st.sidebar.caption("Student Management System")