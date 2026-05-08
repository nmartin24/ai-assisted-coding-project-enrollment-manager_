import streamlit as st
from enrollment_starter import *


def main():
    # Initialize database
    create_tables()
    seed_sample_data()

    # Initialize session state
    if 'user_id' not in st.session_state:
        st.session_state.user_id = CURRENT_STUDENT["user_id"]
    if 'user_name' not in st.session_state:
        st.session_state.user_name = CURRENT_STUDENT["name"]
    if 'role' not in st.session_state:
        st.session_state.role = "student"
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"
    if 'selected_class_id' not in st.session_state:
        st.session_state.selected_class_id = None

    # Page routing
    if st.session_state.current_page == "dashboard":
        show_dashboard()
    elif st.session_state.current_page == "class_details":
        show_class_details()


def show_dashboard():
    st.title("Student Dashboard")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.title("Current Enrolled Classes")
            enrolled = get_student_enrollments(st.session_state.user_id)

            with st.container():
                for course in enrolled:
                    col_class, col_button = st.columns([3, 1])
                    with col_class:
                        st.write(f"**{course['course_name']}**")
                    with col_button:
                        if st.button("Go to class", key=f"go_{course['course_id']}"):
                            st.session_state.current_page = "class_details"
                            st.session_state.selected_class_id = course['course_id']
                            st.rerun()

            enrollment_key = st.text_input("Enter enrollment key to join a class", key="enrollment_key")
            if st.button("Enroll"):
                email = CURRENT_STUDENT["email"]
                result = enroll_with_key(st.session_state.user_id, email, enrollment_key)
                if result:
                    st.success(f"Successfully enrolled in {result['course_id']}!")
                    st.rerun()
                else:
                    st.warning("Invalid enrollment key. Please check and try again.")

    with col2:
        with st.container(border=True):
            st.title("Unenroll")
            enrolled = get_student_enrollments(st.session_state.user_id)
            enrolled_options = [f"{c['course_name']} ({c['course_id']})" for c in enrolled]
            selected = st.selectbox("Select class to unenroll from", enrolled_options, key="unenroll_select")

            if selected:
                course_id = selected.split('(')[-1].strip(')')
                if st.button("Unenroll", key="unenroll_btn"):
                    success = soft_unenroll_student(st.session_state.user_id, course_id)
                    if success:
                        st.info(f"Successfully unenrolled from {selected.split(' (')[0]}.")
                        st.rerun()
                    else:
                        st.error("Failed to unenroll. Please try again.")

            # Mock average grade - in a real app, this would be calculated from actual grades
            st.metric("Average Grade", "92%")


def show_class_details():
    # Get course information
    courses = get_available_course_keys()
    course = next((c for c in courses if c['course_id'] == st.session_state.selected_class_id), None)

    if not course:
        st.error("Class not found.")
        return

    st.title(course['course_name'])

    # Mock data for demonstration - in a real app, this would come from the database
    st.markdown(f"**Teacher:** {course['instructor']}")
    st.markdown(f"**Subject:** {course['course_name']}")
    st.markdown("**Your Grade:** 92%")  # Mock grade
    st.markdown("**Assignments Due:**\n- Assignment 1: Data Analysis Project (Due: May 15, 2026)\n- Assignment 2: Final Presentation (Due: May 20, 2026)")

    if st.button("Back to Dashboard"):
        st.session_state.current_page = "dashboard"
        st.session_state.selected_class_id = None
        st.rerun()


if __name__ == "__main__":
    main()