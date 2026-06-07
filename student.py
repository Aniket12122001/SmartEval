import streamlit as st
import pandas as pd
import json

from database import (
    get_exams,
    get_questions,
    save_result,
    get_results,
    has_attempted_exam
)

from model import calculate_similarity


def student_page():

    # =================================================
    # SECURITY
    # =================================================
    if st.session_state.get("role") != "student":
        st.error("Access Denied")
        st.stop()

    st.markdown("""
    <div class="student-header">
        <h1>🎓 Student Panel</h1>
    </div>
    """, unsafe_allow_html=True)

    menu = st.sidebar.radio(
        "Student Dashboard",
        ["📝 Exams", "📊 Results"]
    )

    # =================================================
    # EXAMS SECTION
    # =================================================
    if menu == "📝 Exams":

        st.markdown("""
        <div class="exam-section">
            <h3>📝 Available Exams</h3>
        </div>
        """, unsafe_allow_html=True)

        student_name = st.session_state.get("username")
        roll_number = st.session_state.get("roll_number")

        exams = get_exams()

        if not exams:
            st.warning("No Exams Available")
            return

        # =================================================
        # ACTIVE EXAM
        # =================================================
        if st.session_state.get("active_exam"):

            exam_id = st.session_state["active_exam"]

            exam = next((e for e in exams if e[0] == exam_id), None)

            if not exam:
                st.error("Exam not found")
                return

            exam_label = f"{exam[3]} - {exam[4]}"

            st.header(f"📝 {exam_label}")

            questions = get_questions(exam_id)

            if not questions:
                st.warning("No Questions Added Yet")
                return

            answers = []

            total_marks = 0
            obtained_marks = 0

            # =================================================
            # QUESTIONS
            # =================================================
            for i, q in enumerate(questions):

                question = q[3]
                reference = q[4]
                marks = float(q[5])

                total_marks += marks

                st.write(f"Q{i+1}. {question}")
                st.write(f"Marks: {marks}")

                answer = st.text_area(
                    "Your Answer",
                    key=f"ans_{i}"
                )

                answers.append({
                    "question": question,
                    "reference": reference,
                    "answer": answer,
                    "marks": marks
                })

                st.divider()

            # =================================================
            # SUBMIT EXAM
            # =================================================
            if st.button("Submit Exam"):

                question_report = []

                for item in answers:

                    result = calculate_similarity(
                        item["answer"],
                        item["reference"]
                    )

                    score = result["score"]

                    obtained = (
                        score / 100
                    ) * item["marks"]

                    obtained_marks += obtained

                    # ================= SAVE QUESTION DATA =================
                    question_report.append({

                        "question": item["question"],

                        "student_answer": item["answer"],

                        "marks": item["marks"],

                        "obtained": round(obtained, 2)

                    })

                # =================================================
                # FINAL PERCENTAGE
                # =================================================
                final_percentage = round(
                    (
                        obtained_marks / total_marks
                    ) * 100 if total_marks else 0,
                    2
                )

                # =================================================
                # GRADE
                # =================================================
                grade = (
                    "A+" if final_percentage >= 90 else
                    "A" if final_percentage >= 80 else
                    "B" if final_percentage >= 70 else
                    "C" if final_percentage >= 60 else
                    "D" if final_percentage >= 50 else
                    "F"
                )

                # =================================================
                # SAVE RESULT
                # =================================================
                save_result((
                    student_name,
                    roll_number,
                    exam_id,
                    exam_label,
                    float(obtained_marks),
                    float(total_marks),
                    final_percentage,
                    grade,
                    json.dumps(question_report)
                ))

                st.success(
                    f"Marks: {round(obtained_marks,2)} / {total_marks}"
                )

                st.success(
                    f"Percentage: {final_percentage}%"
                )

                st.success(
                    f"Grade: {grade}"
                )

                del st.session_state["active_exam"]

                st.rerun()

            return

        # =================================================
        # EXAM LIST
        # =================================================
        for exam in exams:

            exam_label = f"{exam[3]} - {exam[4]}"

            already_attempted = has_attempted_exam(
                roll_number,
                exam[0]
            )

            st.subheader(exam_label)

            if already_attempted:

                st.success("Already Submitted ✅")

                st.button(
                    "Locked 🔒",
                    disabled=True,
                    key=f"done_{exam[0]}"
                )

            else:

                if st.button(
                    f"Start {exam_label}",
                    key=f"start_{exam[0]}"
                ):

                    st.session_state["active_exam"] = exam[0]

                    st.rerun()

    # =================================================
    # RESULTS SECTION
    # =================================================
    elif menu == "📊 Results":
        
        st.markdown("""
        <hr style="
        border:1px solid #E2E8F0;
        margin-top:10px;
        margin-bottom:25px;
        ">
        """, unsafe_allow_html=True)

        st.subheader("📊 My Results")

        roll_number = st.session_state.get("roll_number")

        results = get_results()

        student_results = [

            r for r in results

            if r[2] == roll_number
        ]

        if not student_results:

            st.error("No Results Found")

            return

        # =================================================
        # SUMMARY TABLE
        # =================================================
        st.markdown("## 📋 Exam Summary")

        summary_data = []

        for row in student_results:

            exam_name = row[4]

            obtained = float(row[5] or 0)

            total = float(row[6] or 0)

            percentage = float(row[7] or 0)

            grade = row[8]

            summary_data.append({

                "Exam": exam_name,

                "Marks": f"{round(obtained,2)} / {round(total,2)}",

                "Percentage": f"{percentage}%",

                "Grade": grade
            })

        summary_df = pd.DataFrame(summary_data)

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        st.divider()

        # =================================================
        # RESULT VIEW
        # =================================================
        for row in student_results:

            exam_name = row[4]

            obtained = float(row[5] or 0)

            total = float(row[6] or 0)

            percentage = float(row[7] or 0)

            grade = row[8]

            with st.expander(f"📘 {exam_name}"):

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Obtained Marks",
                        round(obtained, 2)
                        )

                with col2:
                    st.metric(
                        "Total Marks",
                        round(total, 2)
                    )

                with col3:
                    st.metric(
                        "Percentage",
                        f"{percentage}%"
                    )

                with col4:
                    st.metric(
                        "Grade",
                        grade
                    )

                # =================================================
                # QUESTION WISE ANSWERS
                # =================================================
                if len(row) > 9 and row[9]:

                    question_data = json.loads(row[9])

                    for i, q in enumerate(question_data):

                        st.markdown(
                            f"### Q{i+1}. {q['question']}"
                        )

                        st.markdown(
                            f"""
                            <div style="
                                background:white;
                                padding:20px;
                                border-radius:14px;
                                margin-bottom:20px;
                                border:1px solid #E2E8F0;
                                box-shadow:0 2px 8px rgba(0,0,0,0.04);
                            ">

                            <p style="
                                font-size:15px;
                                font-weight:600;
                                color:#2563EB;
                                margin-bottom:10px;
                            ">
                            Student Answer
                            </p>

                            <div style="
                                color:#334155;
                                line-height:1.8;
                                font-size:15px;
                            ">
                                {q['student_answer'].replace('\n', '<br>')}
                            </div>
                            <div style="
                                margin-top:15px;
                                padding-top:10px;
                                border-top:1px solid #E2E8F0;
                                font-weight:600;
                                color:#16A34A;
                            ">

                            Marks Obtained:
                            {q['obtained']} / {q['marks']}

                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )