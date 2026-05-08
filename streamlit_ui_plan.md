# Streamlit UI Plan for Student Enrollment System

## Overview

This plan outlines the implementation of a Streamlit-based user interface for the student enrollment management system. The UI assumes the student is already authenticated and logged in as "John Doe" with user_id "u100" (based on the seeded data in `enrollment_starter.py`). The design follows a multi-layer architecture with clear separation of concerns, ensuring the UI layer calls the service layer with minimal changes to the existing data and service layers.

## Architecture Layers

### Data Layer
The data layer handles all database operations and remains largely unchanged from `enrollment_starter.py`. It consists of pure data access methods that interact directly with the SQLite database.

**Assigned Methods from `enrollment_starter.py`:**
- `connect()` - Establishes database connection
- `create_tables()` - Creates database schema
- `seed_sample_data()` - Populates initial data
- `rows_to_dicts()` - Converts database rows to dictionaries
- `get_available_course_keys()` - Retrieves available enrollment keys
- `get_course_by_key()` - Finds course by enrollment key
- `get_student_enrollments()` - Gets current enrolled classes for a student
- `get_student_enrollment_history()` - Gets all enrollment records for a student
- `get_student_course_record()` - Gets specific enrollment record
- `enroll_with_key()` - Handles enrollment logic (includes some validation that may be moved to service layer)
- `soft_unenroll_student()` - Updates enrollment status to unenrolled
- `get_all_enrollment_records()` - Retrieves all enrollment data for snapshots
- `export_database_snapshot()` - Exports database state to JSON

### Service Layer
The service layer contains business logic, orchestration, and data aggregation. It acts as an intermediary between the UI and data layers, ensuring business rules are enforced and data is properly formatted for presentation.

**Assigned Methods from `enrollment_starter.py`:**
- `get_student_summary()` - Aggregates enrollment statistics

**New Service Methods to Create:**
- `validate_enrollment_key()` - Validates enrollment key format and existence
- `get_student_dashboard_data()` - Orchestrates data retrieval for dashboard display
- `get_class_details()` - Retrieves and formats class information for details page
- `calculate_student_average_grade()` - Computes average grade across enrolled classes

### UI Layer
The UI layer is implemented using Streamlit and handles user interactions, page navigation, and data presentation. It maintains session state and calls service layer methods to retrieve and manipulate data.

**Key Components:**
- Page routing based on `st.session_state`
- Student Dashboard page
- Class Details page
- Error and success message handling

## Session State Management

The UI uses `st.session_state` to manage application state across page reloads:

- `user_id`: "u100" (current student ID)
- `user_name`: "John Doe" (current student name)
- `role`: "student" (user role for future extensibility)
- `current_page`: "dashboard" or "class_details" (controls page navigation)
- `selected_class_id`: Course ID when viewing class details (None for dashboard)

## UI Pages and Implementation Details

### Student Dashboard Page (`current_page == "dashboard"`)

1. **Page Title**: Use `st.title("Student Dashboard")` to display the main page header

2. **Layout Structure**: Use `st.divider()` to visually separate sections

3. **Two-Column Layout**: Use `st.columns(2)` to create left and right columns for content organization

4. **Left Column - Current Enrolled Classes**:
   - Use `st.title("Current Enrolled Classes", anchor=False)` for subsection header
   - Use `st.container()` to group enrolled classes display
   - Retrieve enrolled classes via service layer call to `get_student_enrollments(user_id)`
   - For each enrolled class, display class name and use `st.button(f"Go to class - {class_name}")` 
   - Button click sets `st.session_state.current_page = "class_details"` and `st.session_state.selected_class_id = course_id`

5. **Enrollment Input**: Below the enrolled classes container, use `st.text_input("Enter enrollment key to join a class")` with a submit mechanism

6. **Right Column - Unenroll Section**:
   - Use `st.title("Unenroll", anchor=False)` for subsection header
   - Use `st.selectbox("Select class to unenroll from", options=enrolled_classes_list)` 
   - Selection triggers service layer call to `soft_unenroll_student(user_id, selected_course_id)`
   - Use `st.metric("Average Grade", value=calculated_average)` to display student's average grade across all classes

7. **Enrollment Processing**:
   - On enrollment key submission, call service layer `enroll_with_key(user_id, email, key)`
   - Use `st.success("Successfully enrolled in class!")` for successful enrollment
   - Use `st.warning("Invalid enrollment key. Please check and try again.")` for invalid keys

### Class Details Page (`current_page == "class_details"`)

1. **Page Title**: Use `st.title(class_name)` where class_name is retrieved from the selected course

2. **Class Information Display**:
   - Use `st.markdown(f"**Teacher:** {teacher_name}")` to display instructor
   - Use `st.markdown(f"**Subject:** {subject}")` to display course subject
   - Use `st.markdown(f"**Your Grade:** {grade}")` to display student's grade in the class
   - Use `st.markdown(f"**Assignments Due:** {assignments_list}")` to display pending assignments

3. **Data Generation**: Generate relevant class information including:
   - Teacher name from course instructor field
   - Subject derived from course name
   - Student grade (generate mock grade between 85-95 for demonstration)
   - Assignments due (generate 2-3 mock assignments with due dates)

4. **Navigation**: Include a "Back to Dashboard" button that resets session state to dashboard view

## Error and Success Message Handling

1. **Enrollment Success**: Use `st.success("Successfully enrolled in [class_name]!")` when `enroll_with_key()` returns a valid record

2. **Invalid Enrollment Key**: Use `st.warning("Enrollment key not found. Please check the key and try again.")` when `get_course_by_key()` returns None

3. **Unenrollment Feedback**: Use `st.info("Successfully unenrolled from [class_name].")` after successful unenrollment

4. **General Errors**: Use `st.error("An error occurred. Please try again.")` for unexpected failures

## Implementation Steps

1. **Layer Separation**: Create service layer wrapper functions that call data layer methods and add business logic
2. **Session State Initialization**: Set up initial session state values in the main app function
3. **Page Routing Logic**: Implement conditional rendering based on `st.session_state.current_page`
4. **Dashboard Implementation**: Build the two-column dashboard with enrolled classes and unenroll functionality
5. **Class Details Implementation**: Create the class information display page
6. **Event Handling**: Implement button clicks, form submissions, and state transitions
7. **Testing**: Test enrollment, unenrollment, and navigation flows
8. **Styling**: Apply consistent styling and layout improvements

## Dependencies and Setup

- Ensure `streamlit` is added to `requirements.txt`
- Import existing functions from `enrollment_starter.py` in the appropriate layers
- Initialize database tables and seed data on app startup if needed
- Configure Streamlit settings for proper session management

This plan provides a complete blueprint for implementing the Streamlit UI while maintaining clean architectural separation and leveraging the existing codebase functionality.