import streamlit as st
import pandas as pd

from database import (
    create_user,
    get_teachers,
    get_students,
    get_exams,
    get_results,
    delete_user,
    update_user
)

# =================================================
# 🔐 SECURITY GUARD (PRO UPGRADE)
# =================================================
def require_role(role):
    if st.session_state.get("role") != role:
        st.error("Access Denied")
        st.stop()


def admin_page():

    # 🔐 BLOCK NON-ADMINS
    require_role("admin")

    st.title("🛠 Admin Panel")

    # =================================================
    # DASHBOARD METRICS
    # =================================================
    teachers = get_teachers()
    students = get_students()
    exams = get_exams()
    results = get_results()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Teachers", len(teachers))
    col2.metric("Students", len(students))
    col3.metric("Exams", len(exams))
    col4.metric("Results", len(results))

    st.markdown("---")

    # =================================================
    # SIDEBAR
    # =================================================
    st.sidebar.title("🛠 ADMIN CONTROL PANEL")

    menu = st.sidebar.radio(
        "Select Menu",
        [
            "👤 Create User",
            "👨‍🏫 Manage Teacher",
            "🎓 Manage Student",
            "📊 Student Results",
            "📋 All Users"
        ]
    )

    # =================================================
    # CREATE USER
    # =================================================
    if menu == "👤 Create User":

        st.subheader("👤 Create User")

        username = st.text_input("Username")

        role = st.selectbox(
            "Role",
            ["teacher", "student"]
        )

        roll_number = ""

        if role == "student":
            roll_number = st.text_input("Student Roll Number")
        else:
            roll_number = st.text_input("Teacher ID")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Create User"):

            if username.strip() == "" or password.strip() == "":
                st.error("Fill All Fields")

            elif len(password) < 4:
                st.warning("Password Too Short")

            else:

                created = create_user(
                    username,
                    roll_number,
                    password,
                    role
                )

                if created:
                    st.success(f"{role.title()} Created Successfully")
                else:
                    st.error("User Already Exists")

    # =================================================
    # MANAGE TEACHER
    # =================================================
    elif menu == "👨‍🏫 Manage Teacher":

        st.subheader("👨‍🏫 Manage Teacher")

        teachers = get_teachers()
        exams = get_exams()

        if not teachers:
            st.warning("No Teachers Found")

        else:

            for teacher in teachers:

                teacher_id = teacher[2].strip().lower()

                teacher_exams = [
                    f"{exam[3]} ({exam[4]})"
                    for exam in exams
                    if exam[2].strip().lower() == teacher_id
                ]

                exam_text = ", ".join(teacher_exams) if teacher_exams else "No Exam Created"

                with st.expander(f"Teacher: {teacher[1]} ({teacher[2]})"):

                    st.info(f"Exam Created: {exam_text}")

                    new_username = st.text_input(
                        "Username",
                        value=teacher[1],
                        key=f"teacher_name_{teacher[0]}"
                    )

                    new_password = st.text_input(
                        "Password",
                        value=teacher[3],  # FIXED (was wrong index earlier)
                        key=f"teacher_pass_{teacher[0]}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(
                            "Update",
                            key=f"update_teacher_{teacher[0]}"
                        ):

                            if new_username.strip() == "" or new_password.strip() == "":
                                st.error("Fill All Fields")
                            else:
                                update_user(
                                    teacher[0],
                                    new_username,
                                    teacher[2],
                                    new_password
                                )
                                st.success("Teacher Updated")
                                st.rerun()

                    with col2:
                        if st.button(
                            "Delete",
                            key=f"delete_teacher_{teacher[0]}"
                        ):

                            delete_user(teacher[0])
                            st.warning("Teacher Deleted")
                            st.rerun()

    # =================================================
    # MANAGE STUDENT
    # =================================================
    elif menu == "🎓 Manage Student":

        st.subheader("🎓 Manage Student")

        students = get_students()

        if not students:
            st.warning("No Students Found")

        else:

            for student in students:

                with st.expander(f"Student: {student[1]}"):

                    new_username = st.text_input(
                        "Username",
                        value=student[1],
                        key=f"student_name_{student[0]}"
                    )

                    new_password = st.text_input(
                        "Password",
                        value=student[3],  # FIXED INDEX
                        key=f"student_pass_{student[0]}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(
                            "Update",
                            key=f"update_student_{student[0]}"
                        ):

                            if new_username.strip() == "" or new_password.strip() == "":
                                st.error("Fill All Fields")
                            else:
                                update_user(
                                    student[0],
                                    new_username,
                                    student[2],
                                    new_password
                                )
                                st.success("Student Updated")
                                st.rerun()

                    with col2:
                        if st.button(
                            "Delete",
                            key=f"delete_student_{student[0]}"
                        ):

                            delete_user(student[0])
                            st.warning("Student Deleted")
                            st.rerun()

    # =================================================
    # STUDENT RESULTS
    # =================================================
    elif menu == "📊 Student Results":

        st.subheader("📊 Student Results")

        results = get_results()

        if not results:
            st.warning("No Student Results Found")
            return

        summary = {}

        for row in results:

            student = row[1]
            roll = row[2]
            exam = row[4]
            obtained = float(row[5])
            total = float(row[6])

            key = (student, roll, exam)

            if key not in summary:
                summary[key] = {"obtained": 0, "total": 0}

            summary[key]["obtained"] += obtained
            summary[key]["total"] += total

        final_data = []

        for key, value in summary.items():

            student, roll, exam = key

            obtained_marks = round(value["obtained"], 2)
            total_marks = round(value["total"], 2)

            percentage = round(
                (obtained_marks / total_marks) * 100 if total_marks else 0,
                2
            )

            if percentage >= 90:
                grade = "A+"
            elif percentage >= 80:
                grade = "A"
            elif percentage >= 70:
                grade = "B"
            elif percentage >= 60:
                grade = "C"
            elif percentage >= 50:
                grade = "D"
            else:
                grade = "F"

            final_data.append([
                student,
                roll,
                exam,
                f"{obtained_marks} / {total_marks}",
                f"{percentage}%",
                grade
            ])

        df = pd.DataFrame(
            final_data,
            columns=[
                "Student Name",
                "Roll Number",
                "Exam",
                "Marks",
                "Percentage",
                "Grade"
            ]
        )

        st.dataframe(df, use_container_width=True)

    # =================================================
    # ALL USERS
    # =================================================
    elif menu == "📋 All Users":

        st.subheader("📋 System Users")

        teachers = get_teachers()
        students = get_students()

        all_users = []

        for t in teachers:
            all_users.append([t[0], t[1], t[2], t[4]])

        for s in students:
            all_users.append([s[0], s[1], s[2], s[4]])

        df = pd.DataFrame(
            all_users,
            columns=[
                "DB_ID",
                "Username",
                "Unique ID",
                "Role"
            ]
        )
        # Create clean serial numbers
        df.insert(0, "ID", range(1, len(df) + 1))

        # Remove actual database id
        df = df.drop(columns=["DB_ID"])

        st.dataframe(df, use_container_width=True,hide_index=True)