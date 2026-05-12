import pandas as pd
import streamlit as st 


def student_dashboard_core():
    student_data = pd.DataFrame({
        ":material/id_card: ID Number": ["2025-0000", "2025-0001", "2025-0002"], 
        ":material/school: Students": [
            "John Carl Acosta",
            "Kerby Andres",
            "Justin Paul Obera"
        ],
        ":material/grading: GWA": [1.5, 1.5, 1.4],
        ":material/info: Enrollment Status": ["Enrolled", "Enrolled", "Enrolled"],
        ":material/book_5: Course": ["BSIT", "BSIT", "BSIT"]
    })

    st.table(student_data)
    



#starter
student_dashboard_core()