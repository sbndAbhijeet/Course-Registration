import sqlite3

# Connect to the SQLite database (replace 'db.sqlite3' with your actual database file)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


# Student table (accounts_student)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts_student (
        email TEXT PRIMARY KEY,
        student_name TEXT NOT NULL
        -- Add other fields like college_id if present in your Student model
    )
""")

# Faculty table (accounts_faculty)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts_faculty (
        email TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
""")

# Course table (course_registration_course)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_registration_course (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        semester INTEGER NOT NULL,
        course_code TEXT NOT NULL DEFAULT 'Unknown',
        name TEXT NOT NULL,
        credits TEXT NOT NULL,
        branch_name TEXT NOT NULL DEFAULT 'CSE/IT'
    )
""")

# StudentRegistration table (course_registration_studentregistration)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_registration_studentregistration (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        previous_spi REAL NOT NULL,
        previous_cpi REAL NOT NULL,
        branch_name TEXT NOT NULL DEFAULT 'CSE/IT',
        semester_applying_for TEXT NOT NULL,
        faculty_email TEXT,
        grade_sheet TEXT,
        college_fee_proof TEXT NOT NULL,
        hostel_fee_proof TEXT NOT NULL,
        loan_refund_form TEXT,
        submitted_at TIMESTAMP,
        status TEXT NOT NULL DEFAULT 'In Progress',
        message TEXT,
        FOREIGN KEY (student_email) REFERENCES accounts_student(email),
        FOREIGN KEY (faculty_email) REFERENCES accounts_faculty(email)
    )
""")

# Junction table for StudentRegistration selected_courses
cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_registration_studentregistration_selected_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        studentregistration_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        FOREIGN KEY (studentregistration_id) REFERENCES course_registration_studentregistration(id),
        FOREIGN KEY (course_id) REFERENCES course_registration_course(id),
        UNIQUE (studentregistration_id, course_id)
    )
""")

# Enrolled table (course_registration_enrolled)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_registration_enrolled (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL UNIQUE,
        faculty_email TEXT,
        FOREIGN KEY (student_id) REFERENCES accounts_student(email),
        FOREIGN KEY (faculty_email) REFERENCES accounts_faculty(email)
    )
""")

# Junction table for Enrolled selected_courses
cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_registration_enrolled_selected_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enrolled_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        FOREIGN KEY (enrolled_id) REFERENCES course_registration_enrolled(id),
        FOREIGN KEY (course_id) REFERENCES course_registration_course(id),
        UNIQUE (enrolled_id, course_id)
    )
""")

# --- Trigger: Automatically set submitted_at on insert ---
cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS set_submitted_at
    AFTER INSERT ON course_registration_studentregistration
    FOR EACH ROW
    BEGIN
        UPDATE course_registration_studentregistration
        SET submitted_at = CURRENT_TIMESTAMP
        WHERE id = NEW.id;
    END;
""")

# --- Indexes for performance ---
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_student_email 
    ON course_registration_studentregistration(student_email)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_semester_branch 
    ON course_registration_course(semester, branch_name)
""")

# --- Sample Data Insertion ---

# Insert a student
cursor.execute("""
    INSERT OR IGNORE INTO accounts_student (email, student_name)
    VALUES (?, ?)
""", ('202351127@iiitvadodara.ac.in', 'Student Name'))

# Insert a faculty
cursor.execute("""
    INSERT OR IGNORE INTO accounts_faculty (email, name)
    VALUES (?, ?)
""", ('faculty@iiitvadodara.ac.in', 'Faculty Name'))

# Insert some courses
courses = [
    (1, 'CS101', 'Intro to CS', '3-0-0 : 3', 'CSE'),
    (1, 'IT101', 'Intro to IT', '3-0-0 : 3', 'IT'),
    (2, 'CS201', 'Data Structures', '3-1-0 : 4', 'CSE'),
]
for course in courses:
    cursor.execute("""
        INSERT OR IGNORE INTO course_registration_course (semester, course_code, name, credits, branch_name)
        VALUES (?, ?, ?, ?, ?)
    """, course)

# --- Simulate register_student View ---

# Fetch student (equivalent to get_object_or_404)
student_email = '202351127@iiitvadodara.ac.in'
cursor.execute("""
    SELECT email, student_name FROM accounts_student WHERE email = ?
""", (student_email,))
student = cursor.fetchone()
if not student:
    raise ValueError("Student not found")

# Check existing registration (StudentRegistration.objects.filter(student=student).first())
cursor.execute("""
    SELECT id FROM course_registration_studentregistration WHERE student_email = ?
""", (student_email,))
existing_registration = cursor.fetchone()

if existing_registration:
    registration_id = existing_registration[0]
    # Update existing registration (simplified)
    cursor.execute("""
        UPDATE course_registration_studentregistration
        SET previous_spi = ?, previous_cpi = ?, semester_applying_for = ?, faculty_email = ?,
            grade_sheet = ?, college_fee_proof = ?, hostel_fee_proof = ?, loan_refund_form = ?
        WHERE id = ?
    """, (
        8.5, 8.0, '2', 'faculty@iiitvadodara.ac.in',
        'fee_documents/grade.pdf', 'fee_documents/college_fee.pdf', 
        'fee_documents/hostel_fee.pdf', 'fee_documents/loan.pdf',
        registration_id
    ))
else:
    # Insert new registration
    cursor.execute("""
        INSERT INTO course_registration_studentregistration (
            student_email, name, email, previous_spi, previous_cpi,
            branch_name, semester_applying_for, faculty_email,
            grade_sheet, college_fee_proof, hostel_fee_proof,
            loan_refund_form, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'In Progress')
    """, (
        student_email, 'Student Name', student_email, 8.5, 8.0,
        'CSE', '2', 'faculty@iiitvadodara.ac.in',
        'fee_documents/grade.pdf', 'fee_documents/college_fee.pdf', 
        'fee_documents/hostel_fee.pdf', 'fee_documents/loan.pdf'
    ))
    registration_id = cursor.lastrowid

# Save selected courses (form.save_m2m())
selected_course_ids = [1, 3]  # Example course IDs from form
cursor.execute("""
    DELETE FROM course_registration_studentregistration_selected_courses 
    WHERE studentregistration_id = ?
""", (registration_id,))
for course_id in selected_course_ids:
    cursor.execute("""
        INSERT OR IGNORE INTO course_registration_studentregistration_selected_courses 
        (studentregistration_id, course_id)
        VALUES (?, ?)
    """, (registration_id, course_id))

# Handle Enrolled (Enrolled.objects.get_or_create)
cursor.execute("""
    SELECT id FROM course_registration_enrolled WHERE student_id = ?
""", (student_email,))
enrolled_row = cursor.fetchone()

if enrolled_row:
    enrolled_id = enrolled_row[0]
else:
    cursor.execute("""
        INSERT INTO course_registration_enrolled (student_id, faculty_email)
        VALUES (?, ?)
    """, (student_email, 'faculty@iiitvadodara.ac.in'))
    enrolled_id = cursor.lastrowid

# Update Enrolled selected_courses
cursor.execute("""
    DELETE FROM course_registration_enrolled_selected_courses WHERE enrolled_id = ?
""", (enrolled_id,))
for course_id in selected_course_ids:
    cursor.execute("""
        INSERT OR IGNORE INTO course_registration_enrolled_selected_courses 
        (enrolled_id, course_id)
        VALUES (?, ?)
    """, (enrolled_id, course_id))

# Update faculty in Enrolled
cursor.execute("""
    UPDATE course_registration_enrolled
    SET faculty_email = ?
    WHERE id = ?
""", ('faculty@iiitvadodara.ac.in', enrolled_id))

# --- Simulate registration_success View ---

# Fetch registration details
cursor.execute("""
    SELECT * FROM course_registration_studentregistration 
    WHERE id = ? AND student_email = ?
""", (registration_id, student_email))
registration = cursor.fetchone()
print("Registration Details:", registration)

# Note: Email sending is handled by Django, not SQL

# --- Simulate get_courses View ---

semester = '1'
branch = 'CSE'
if branch == 'CSE/IT':
    cursor.execute("""
        SELECT id, course_code, name, credits
        FROM course_registration_course
        WHERE semester = ? AND branch_name IN ('CSE', 'IT')
    """, (semester,))
else:
    cursor.execute("""
        SELECT id, course_code, name, credits
        FROM course_registration_course
        WHERE semester = ? AND branch_name = ?
    """, (semester, branch))
courses = cursor.fetchall()
print("Courses for Semester and Branch:", courses)

# --- Additional Project-Specific Queries ---

# Fetch all registrations for a student
cursor.execute("""
    SELECT id, semester_applying_for, status 
    FROM course_registration_studentregistration 
    WHERE student_email = ?
""", (student_email,))
all_registrations = cursor.fetchall()
print("All Registrations for Student:", all_registrations)

# Fetch selected courses for a registration
cursor.execute("""
    SELECT c.course_code, c.name
    FROM course_registration_course c
    JOIN course_registration_studentregistration_selected_courses sc 
    ON c.id = sc.course_id
    WHERE sc.studentregistration_id = ?
""", (registration_id,))
selected_courses = cursor.fetchall()
print("Selected Courses for Registration:", selected_courses)

# Fetch enrolled courses for a student
cursor.execute("""
    SELECT c.course_code, c.name
    FROM course_registration_course c
    JOIN course_registration_enrolled_selected_courses ec 
    ON c.id = ec.course_id
    JOIN course_registration_enrolled e ON ec.enrolled_id = e.id
    WHERE e.student_id = ?
""", (student_email,))
enrolled_courses = cursor.fetchall()
print("Enrolled Courses for Student:", enrolled_courses)

# Fetch faculty advisors (Faculty.objects.all())
cursor.execute("""
    SELECT email, name FROM accounts_faculty
""")
faculty_advisors = cursor.fetchall()
print("Faculty Advisors:", faculty_advisors)

# Commit changes and close connection
conn.commit()
conn.close()