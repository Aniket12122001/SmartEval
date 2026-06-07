import streamlit as st

from admin_page import admin_page
from teacher import teacher_page
from student import student_page
from database import login


# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="SmartEval",
    page_icon="🧠",
    layout="wide"
)


# =================================================
# LOAD CSS
# =================================================
def load_css():

    with open("style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# =================================================
# SESSION INITIALIZATION
# =================================================
if "role" not in st.session_state:
    st.session_state["role"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "roll_number" not in st.session_state:
    st.session_state["roll_number"] = None    

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "active_exam" not in st.session_state:
    st.session_state["active_exam"] = None


# =================================================
# LOGIN PAGE
# =================================================
if st.session_state["role"] is None:

    st.markdown(
        """
        <h1 style='text-align:center; font-size:50px;'>
        🧠 SmartEval
        </h1>

        <p style='text-align:center; font-size:18px; color:gray; margin-top:-15px;'>
        AI-Powered Smart Exam Evaluation Platform
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.subheader("🔐 Login")

        role = st.selectbox(
            "Login As",
            ["admin", "teacher", "student"]
        )

        if role == "student":

            username = st.text_input("Student Roll Number")
        
        elif role == "teacher":

             username = st.text_input("Teacher ID")    

        else:

            username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            # ================= ADMIN =================
            if role == "admin":

                if username == "admin" and password == "Admin@123":

                    st.session_state["role"] = "admin"
                    st.session_state["username"] = "admin"
                    st.session_state["logged_in"] = True

                    st.rerun()

                else:
                    st.error("Invalid Admin Credentials")

            # ================= TEACHER =================
            elif role == "teacher":

                user = login(username, password, role)

                if user:

                    st.session_state["role"] = "teacher"
                    st.session_state["username"] = user[1]
                    st.session_state["roll_number"] = user[2]
                    st.session_state["logged_in"] = True

                    st.rerun()

                else:
                    st.error("Invalid Teacher Credentials")

            # ================= STUDENT =================
            elif role == "student":

                user = login(username, password, role)

                if user:

                    st.session_state["role"] = "student"
                    st.session_state["username"] = user[1]
                    st.session_state["roll_number"] = user[2]
                    st.session_state["logged_in"] = True

                    st.rerun()

                else:
                    st.error("Invalid Student Credentials")


# =================================================
# DASHBOARD ROUTING
# =================================================
else:

    role = st.session_state.get("role")
    logged_in = st.session_state.get("logged_in", False)

    # ================= SAFETY =================
    if not logged_in:

        st.warning("Session Invalid. Please Login Again.")

        st.session_state.clear()

        st.rerun()

    # ================= ADMIN =================
    if role == "admin":

        admin_page()

        st.sidebar.markdown("---")

        if st.sidebar.button("Logout"):

            st.session_state.clear()
            st.rerun()

    # ================= TEACHER =================
    elif role == "teacher":

        teacher_page()

        st.sidebar.markdown("---")

        if st.sidebar.button("Logout"):

            st.session_state.clear()
            st.rerun()

    # ================= STUDENT =================
    elif role == "student":

        student_page()

        st.sidebar.markdown("---")

        if st.sidebar.button("Logout"):

            st.session_state.clear()
            st.rerun()