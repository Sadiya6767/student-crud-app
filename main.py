from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, status

from database import (
    init_db,
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    patch_student,
    delete_student
)
from models import (
    StudentCreate,
    StudentUpdate,
    StudentPatch,
    StudentResponse
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager:
    Ensures SQLite tables are created automatically before the app starts handling requests.
    """
    init_db()
    yield


# Automatically create table on module import as well as during app lifespan
init_db()

# Initialize FastAPI application with informative metadata
app = FastAPI(
    title="Student Database CRUD Application",
    description="Backend API for managing student records using FastAPI and SQLite.",
    version="1.0.0",
    lifespan=lifespan
)


# Helper function to convert Pydantic date objects to ISO strings for SQLite
def prepare_student_dict_for_db(student_model: StudentCreate) -> dict:
    data = student_model.model_dump()
    if data.get("date_of_birth"):
        data["date_of_birth"] = str(data["date_of_birth"])
    if data.get("enrollment_date"):
        data["enrollment_date"] = str(data["enrollment_date"])
    return data


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Returns empty 204 response so browser favicon requests don't show 404."""
    from fastapi.responses import Response
    return Response(status_code=204)


@app.get("/", tags=["General"])
def root():
    """
    Root endpoint: Automatically redirects browser to interactive Swagger UI (/docs)
    while returning 200 OK.
    """
    from fastapi.responses import HTMLResponse
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Database CRUD Application</title>
        <meta http-equiv="refresh" content="0; url=/docs" />
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f4f6f8; margin: 0; }
            .card { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); text-align: center; max-width: 480px; }
            h2 { color: #1a202c; margin-bottom: 8px; }
            p { color: #4a5568; margin-bottom: 24px; font-size: 15px; }
            .btn { display: inline-block; padding: 12px 28px; background: #2563eb; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; transition: background 0.2s; }
            .btn:hover { background: #1d4ed8; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🎓 Student Database CRUD Application</h2>
            <p>EWB Edu Tech Pvt. Ltd. Internship Assignment</p>
            <p>Opening Swagger Interactive API Documentation...</p>
            <a class="btn" href="/docs">Click here if not redirected to /docs</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# ---------------------------------------------------------------------------
# 1. CREATE: POST /students
# ---------------------------------------------------------------------------
@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
    summary="Create a new student record"
)
def add_student(student: StudentCreate):
    """
    Add a new student to the database.
    - **name**: Required (non-empty string)
    - **date_of_birth**: Required (format: YYYY-MM-DD)
    - **email** or **phone**: At least one must be provided
    - **course**, **address**, **enrollment_date**: Optional
    """
    # Prepare data dictionary with formatted dates
    student_dict = prepare_student_dict_for_db(student)

    # Insert into database and obtain the auto-generated ID
    new_student_id = create_student(student_dict)

    # Retrieve and return the created student
    created_student = get_student_by_id(new_student_id)
    return created_student


# ---------------------------------------------------------------------------
# 2. READ ALL: GET /students
# ---------------------------------------------------------------------------
@app.get(
    "/students",
    response_model=List[StudentResponse],
    status_code=status.HTTP_200_OK,
    tags=["Students"],
    summary="Retrieve all student records"
)
def list_students():
    """
    Retrieve a list of all students currently stored in the database.
    Returns an empty list `[]` if no students exist.
    """
    students = get_all_students()
    return students


# ---------------------------------------------------------------------------
# 3. READ ONE: GET /students/{student_id}
# ---------------------------------------------------------------------------
@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Students"],
    summary="Retrieve one student by ID"
)
def get_student(student_id: int):
    """
    Retrieve the details of a single student using their unique integer ID.
    Returns 404 if the student ID is not found.
    """
    student = get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} was not found."
        )
    return student


# ---------------------------------------------------------------------------
# 4. UPDATE (FULL): PUT /students/{student_id}
# ---------------------------------------------------------------------------
@app.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Students"],
    summary="Update an existing student's details (Full update)"
)
def replace_student(student_id: int, student: StudentUpdate):
    """
    Completely updates an existing student record.
    Follows standard PUT semantics: all required fields must be supplied.
    Returns 404 if the student ID is not found.
    """
    # Check if student exists
    existing = get_student_by_id(student_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} was not found."
        )

    # Prepare data dictionary and perform update
    student_dict = prepare_student_dict_for_db(student)
    update_student(student_id, student_dict)

    # Return updated student record
    updated_student = get_student_by_id(student_id)
    return updated_student


# ---------------------------------------------------------------------------
# 5. UPDATE (PARTIAL): PATCH /students/{student_id}
# ---------------------------------------------------------------------------
@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Students"],
    summary="Partially update an existing student's details"
)
def modify_student(student_id: int, student_patch: StudentPatch):
    """
    Selectively updates only the fields provided in the request body.
    Unprovided fields remain unchanged in the database.
    Returns 404 if the student ID is not found.
    """
    # Check if student exists
    existing = get_student_by_id(student_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} was not found."
        )

    # Extract only fields that were explicitly sent by the client
    patch_data = student_patch.model_dump(exclude_unset=True)

    # If no fields were provided, return existing student as-is
    if not patch_data:
        return existing

    # Validate that at least one of email or phone remains after the update
    resulting_email = patch_data.get("email", existing["email"])
    resulting_phone = patch_data.get("phone", existing["phone"])

    if not resulting_email and not resulting_phone:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Student must retain at least one contact method: 'email' or 'phone'."
        )

    # Format date fields to string for SQLite if present
    if "date_of_birth" in patch_data and patch_data["date_of_birth"] is not None:
        patch_data["date_of_birth"] = str(patch_data["date_of_birth"])
    if "enrollment_date" in patch_data and patch_data["enrollment_date"] is not None:
        patch_data["enrollment_date"] = str(patch_data["enrollment_date"])

    # Apply partial update to SQLite
    patch_student(student_id, patch_data)

    # Return updated student
    updated_student = get_student_by_id(student_id)
    return updated_student


# ---------------------------------------------------------------------------
# 6. DELETE: DELETE /students/{student_id}
# ---------------------------------------------------------------------------
@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_200_OK,
    tags=["Students"],
    summary="Delete a student record"
)
def remove_student(student_id: int):
    """
    Deletes a student record by ID.
    Returns 404 if the student ID is not found.
    """
    # Check if student exists before attempting deletion
    existing = get_student_by_id(student_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} was not found."
        )

    # Delete record from database
    delete_student(student_id)

    return {
        "message": f"Student with ID {student_id} was deleted successfully."
    }
