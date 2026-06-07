import streamlit as st
from database import get_results
import pandas as pd


def result_page():

    st.title("📊 Overall Student Results")

    data = get_results()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Student",
            "Roll",
            "Exam",
            "Total Marks",
            "Percentage",
            "Grade"
        ]
    )

    # Hide ID column
    df = df.drop(columns=["ID"])

    st.dataframe(df, use_container_width=True)