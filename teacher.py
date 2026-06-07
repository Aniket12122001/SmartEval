import streamlit as st
import pandas as pd
import json

from database import (
    add_exam,
    get_exams,
    add_question,
    get_questions,
    get_results,
    delete_exam,
    update_question,
    delete_question
)


def teacher_page():

    # ================================
    # SECURITY CHECK
    # ================================
    if st.session_state.get("role") != "teacher":
        st.error("Access Denied")
        st.stop()

    teacher_name = st.session_state.get("username")
    teacher_id = st.session_state.get("roll_number")

    if not teacher_name or not teacher_id:
        st.error("Session expired. Please login again.")
        return

    st.title("👨‍🏫 Teacher Panel")

    # ================================
    # SIDEBAR MENU
    # ================================
    menu = st.sidebar.radio(
        "Teacher Dashboard",
        [
            "📝 Create Exam",
            "❓ Manage Questions",
            "📊 View Results"
        ]
    )

    # =================================================
    # CREATE EXAM
    # =================================================
    if menu == "📝 Create Exam":

        st.subheader("📝 Create New Exam")

        subject = st.text_input("Subject Name")
        exam_name = st.text_input("Exam Name")

        if st.button("Create Exam"):

            if subject and exam_name:

                add_exam(
                    teacher_name,
                    teacher_id,
                    subject,
                    exam_name
                )

                st.success("Exam Created Successfully")

            else:
                st.error("Fill All Fields")

        st.divider()

        st.subheader("📚 Existing Exams")

        exams = get_exams(teacher_id)

        if exams:

            for exam in exams:

                exam_id = exam[0]
                label = f"{exam[3]} - {exam[4]}"

                col1, col2 = st.columns([5, 1])

                with col1:
                    st.info(label)

                with col2:

                    if st.button(
                        "Delete",
                        key=f"delete_exam_{exam_id}"
                    ):

                        delete_exam(exam_id, teacher_id)

                        st.success("Exam Deleted")
                        st.rerun()

        else:
            st.warning("No Exams Found")

    # =================================================
    # MANAGE QUESTIONS
    # =================================================
    elif menu == "❓ Manage Questions":

        st.subheader("❓ Manage Questions")

        exams = get_exams(teacher_id)

        if not exams:
            st.warning("No Exams Available")
            return

        exam_options = {
            f"{exam[3]} - {exam[4]}": exam[0]
            for exam in exams
        }

        selected_exam = st.selectbox(
            "Select Exam",
            list(exam_options.keys())
        )

        exam_id = exam_options[selected_exam]

        # ================= ADD QUESTION =================
        st.divider()

        st.subheader("➕ Add Question")

        question = st.text_area("Question")

        reference_answer = st.text_area(
            "Reference Answer"
        )

        marks = st.number_input(
            "Marks",
            min_value=1,
            max_value=20
        )

        if st.button("Add Question"):

            if question and reference_answer:

                add_question(
                    exam_id,
                    selected_exam,
                    question,
                    reference_answer,
                    marks
                )

                st.success("Question Added")
                st.rerun()

            else:
                st.error("Fill All Fields")

        # ================= VIEW QUESTIONS =================
        st.divider()

        st.subheader("📄 Existing Questions")

        questions = get_questions(exam_id)

        if not questions:
            st.warning("No Questions Found")
            return

        for q in questions:

            question_id = q[0]

            st.markdown("---")

            new_question = st.text_area(
                "Question",
                value=q[3],
                key=f"q_{question_id}"
            )

            new_reference = st.text_area(
                "Reference Answer",
                value=q[4],
                key=f"r_{question_id}"
            )

            new_marks = st.number_input(
                "Marks",
                min_value=1,
                max_value=20,
                value=int(q[5]),
                key=f"m_{question_id}"
            )

            col1, col2 = st.columns(2)

            # ================= UPDATE =================
            with col1:

                if st.button(
                    "Update",
                    key=f"update_{question_id}"
                ):

                    update_question(
                        question_id,
                        new_question,
                        new_reference,
                        new_marks
                    )

                    st.success("Question Updated")
                    st.rerun()

            # ================= DELETE =================
            with col2:

                if st.button(
                    "Delete",
                    key=f"delete_{question_id}"
                ):

                    delete_question(question_id)

                    st.success("Question Deleted")
                    st.rerun()

    # =================================================
    # VIEW RESULTS
    # =================================================
    elif menu == "📊 View Results":

        st.subheader("📊 Final Results")

        exams = get_exams(teacher_id)

        if not exams:
            st.warning("No Exams Available")
            return

        exam_map = {
            f"{e[3]} - {e[4]}": e[0]
            for e in exams
        }

        selected_exam = st.selectbox(
            "Select Exam",
            list(exam_map.keys())
        )

        results = get_results()

        filtered = [
            r for r in results
            if r[4] == selected_exam
        ]

        if not filtered:
            st.warning("No Results Found")
            return

        # =================================================
        # SUMMARY TABLE
        # =================================================
        final_data = []

        for r in filtered:

            student_name = r[1]
            roll_number = r[2]

            obtained = float(r[5])
            total = float(r[6])

            percentage = float(r[7])
            grade = r[8]

            final_data.append([
                student_name,
                roll_number,
                f"{obtained} / {total}",
                f"{percentage}%",
                grade
            ])

        df = pd.DataFrame(
            final_data,
            columns=[
                "Student",
                "Roll",
                "Marks",
                "Percentage",
                "Grade"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        