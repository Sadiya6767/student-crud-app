"""
seed.py - Optional script to populate the database with realistic sample dummy student records.
Safe to run multiple times: skips insertion if student records already exist.
"""

from database import init_db, get_all_students, create_student


SAMPLE_STUDENTS = [
    {
        "name": "Rahul Sharma",
        "date_of_birth": "2002-08-14",
        "email": "rahul.sharma@example.com",
        "phone": "9876543210",
        "course": "Computer Science Engineering",
        "address": "Sector 62, Noida, Uttar Pradesh",
        "enrollment_date": "2024-07-15"
    },
    {
        "name": "Priya Patel",
        "date_of_birth": "2003-03-22",
        "email": "priya.patel@example.com",
        "phone": "9812345678",
        "course": "Information Technology",
        "address": "Vastrapur, Ahmedabad, Gujarat",
        "enrollment_date": "2024-07-20"
    },
    {
        "name": "Amit Verma",
        "date_of_birth": "2001-11-05",
        "email": "amit.verma@example.com",
        "phone": "9988776655",
        "course": "Electronics and Communication",
        "address": "Kothrud, Pune, Maharashtra",
        "enrollment_date": "2024-08-01"
    }
]


def seed_data():
    # Make sure table exists
    init_db()

    existing_students = get_all_students()
    if len(existing_students) > 0:
        print(f"[INFO] Database already contains {len(existing_students)} student record(s).")
        print("[INFO] Skipping seeding to prevent duplicate records.")
        return

    print("[INFO] Seeding sample dummy student records into SQLite database...")
    for student in SAMPLE_STUDENTS:
        new_id = create_student(student)
        print(f"  + Added student: {student['name']} (Assigned ID: {new_id})")

    print("[SUCCESS] Sample students added successfully! Total:", len(SAMPLE_STUDENTS))


if __name__ == "__main__":
    seed_data()
