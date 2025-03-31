import pandas as pd
from models import ClassSchedule

# Mapping of course codes to semesters (from UG Curriculum PDF)
COURSE_SEMESTER_MAPPING = {
    # Semester I
    'MA101': 1, 'PH100': 1, 'PH160': 1, 'IT101': 1, 'IT161': 1, 'EC100': 1, 'EC160': 1, 'HS101': 1,
    # Semester II
    'MA102': 2, 'PH110': 2, 'PH170': 2, 'EE100': 2, 'EE160': 2, 'CS102': 2, 'CS162': 2, 'HS102': 2,
    # Semester III
    'MA201': 3, 'CS201': 3, 'CS261': 3, 'CS203': 3, 'CS263': 3, 'CS204': 3, 'HS201': 3, 'SC201': 3,
    # Semester IV
    'MA202': 4, 'CS202': 4, 'CS262': 4, 'CS205': 4, 'CS265': 4, 'CS206': 4, 'CS266': 4, 'HS202': 4,
    # Semester V
    'CS301': 5, 'CS361': 5, 'CS303': 5, 'CS363': 5, 'CS305': 5,
    # Semester VI
    'CS302': 6, 'CS362': 6, 'CS304': 6, 'CS364': 6,
    # Semester VII
    'CS401': 7, 'CS461': 7, 'CS491': 7,
    # Semester VIII
    'CS490': 8, 'IT490': 8,
}

def populate_schedule(excel_file_path):
    # Read the Excel file (assuming both sheets have the same structure)
    xl = pd.ExcelFile(excel_file_path)
    for sheet_name in xl.sheet_names:
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

        # Iterate over each row (each row represents a room's schedule for a day)
        for index, row in df.iterrows():
            day = row['Day']
            room = row['Room']
            room_capacity = row['Cap #']
            actual_students = row['Act #']

            # Iterate over time slots (columns from 9:15 to 17:30)
            for col in df.columns:
                if col in ['Day', 'Room', 'Cap #', 'Act #']:
                    continue  # Skip non-time columns

                cell_value = row[col]
                time_slot = col  # e.g., "9:15"

                # If cell is not empty and contains a course code
                if pd.notna(cell_value) and isinstance(cell_value, str):
                    course_info = cell_value.strip().split()
                    if len(course_info) >= 1:
                        course_code = course_info[0]
                        section = course_info[1] if len(course_info) > 1 else None

                        # Get the semester for the course code
                        semester = COURSE_SEMESTER_MAPPING.get(course_code, 0)
                        if semester:
                            # Create a ClassSchedule entry for this time slot
                            ClassSchedule.objects.create(
                                day=day,
                                room=room,
                                room_capacity=room_capacity,
                                actual_students=actual_students,
                                course_code=course_code,
                                section=section,
                                semester=semester,
                                time_slot=time_slot
                            )

if __name__ == "__main__":
    # Replace with the path to your Excel file
    excel_file_path = "C:/Users/sbnda/Downloads/ClassSchedules.xlsx"
    populate_schedule(excel_file_path)