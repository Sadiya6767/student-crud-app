# Student Database CRUD Application

**Internship Project Assignment**  
**Company:** EWB Edu Tech Pvt. Ltd.  
**Role:** Python Backend Development Intern  
**Tech Stack:** Python 3, FastAPI, SQLite (built-in `sqlite3`), Uvicorn, Pydantic  

---

## 1. Project Overview

The **Student Database CRUD Application** is a lightweight, beginner-friendly RESTful backend API designed to manage student records. It implements all four core database operations: **Create, Read, Update, and Delete (CRUD)**.

The project is built specifically to demonstrate core backend fundamentals:
- Building clean REST APIs with **FastAPI**.
- Performing database operations using Python's native **`sqlite3`** module without heavy ORMs.
- Securing SQL queries against SQL injection using **parameterized queries**.
- Enforcing strong schema validation with **Pydantic**.
- Providing interactive documentation via **Swagger UI** (`/docs`).

---

## 2. Key Features

- **Automatic Database Setup:** Automatically creates the SQLite database file (`students.db`) and table on startup.
- **Full CRUD Endpoints:** Supports creating, listing, fetching by ID, full updates (PUT), partial updates (PATCH), and deleting students.
- **Reliable Data Persistence:** All records are stored in a local SQLite file that survives application restarts.
- **Strict Data Validation:**
  - `name` is required and cannot be empty or whitespace only.
  - `date_of_birth` is required and strictly validated in `YYYY-MM-DD` format.
  - At least one contact method (`email` or `phone`) must be supplied.
  - Email addresses are validated for standard syntax.
- **SQL Injection Prevention:** 100% of database queries use SQLite `?` parameter placeholders.
- **Accurate HTTP Status Codes:** Returns `201 Created`, `200 OK`, `404 Not Found`, and `422 Unprocessable Entity`.
- **Interactive Swagger Documentation:** Explore and test all endpoints directly from your browser.
- **Safe Seeding Script:** Includes `seed.py` with realistic dummy data that avoids duplicating existing records.

---

## 3. Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10+** | Core programming language |
| **FastAPI** | Modern, fast web framework for building APIs |
| **SQLite (`sqlite3`)** | Lightweight, zero-config relational database (Python built-in) |
| **Uvicorn** | Lightning-fast ASGI web server |
| **Pydantic v2** | Data parsing, type enforcement, and request validation |

---

## 4. Project Folder Structure

```text
student-crud-app/
├── database.py         # SQLite connection manager, table creation, and CRUD SQL queries
├── main.py             # FastAPI application, endpoint routing, and HTTP response handling
├── models.py           # Pydantic models for request validation and response schemas
├── seed.py             # Optional script to insert realistic dummy student data
├── test_api.py         # Automated test script verifying all 16 endpoint behaviors
├── requirements.txt    # Project dependencies
├── .gitignore          # Excludes virtual environments, cache, and local database files
└── README.md           # Complete documentation and setup guide
```

---

## 5. Prerequisites

Before running this project, ensure you have **Python 3.10 or higher** installed on your system.

Check your Python version by opening a terminal or PowerShell prompt:
```powershell
python --version
```

---

## 6. Installation & Setup Guide

Follow these step-by-step instructions to set up and run the application locally on your Windows machine:

### Step 1: Open Terminal in the Project Directory

Navigate into the `student-crud-app` folder:
```powershell
cd c:\Users\sadiya\Downloads\mis\student-crud-app
```

### Step 2: Create a Virtual Environment

It is recommended to isolate project dependencies inside a virtual environment:
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment

- **On Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(Note: If PowerShell shows an Execution Policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first)*

- **On Windows (Command Prompt `cmd`):**
  ```cmd
  venv\Scripts\activate.bat
  ```

- **On macOS / Linux (Bash / Zsh):**
  ```bash
  source venv/bin/activate
  ```

### Step 4: Install Dependencies

Install the required packages from `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### Step 5: (Optional) Seed Sample Data

To pre-fill the database with realistic sample dummy student records:
```powershell
python seed.py
```
*Note: This script safely checks if records already exist and will not insert duplicate records.*

---

## 7. Running the Application

Start the local development server with Uvicorn:

```powershell
uvicorn main:app --reload
```

The output will confirm the server is running:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

---

## 8. Interactive API Documentation (Swagger UI)

Once the application is running, open your web browser and visit:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

From Swagger UI, click **"Try it out"** on any endpoint to send live requests and view formatted responses.

---

## 9. API Endpoints Summary

| Method | Endpoint | Status Code | Description |
| :--- | :--- | :---: | :--- |
| `GET` | `/` | `200 OK` | Project information and link to Swagger documentation |
| `POST` | `/students` | `201 Created` | Create a new student record |
| `GET` | `/students` | `200 OK` | Retrieve all student records |
| `GET` | `/students/{student_id}` | `200 OK` / `404 Not Found` | Retrieve a single student by ID |
| `PUT` | `/students/{student_id}` | `200 OK` / `404 Not Found` | Fully replace an existing student record |
| `PATCH`| `/students/{student_id}` | `200 OK` / `404 Not Found` | Partially update specific student fields |
| `DELETE`| `/students/{student_id}` | `200 OK` / `404 Not Found` | Delete a student by ID |

---

## 10. Sample Request Bodies & Responses

### 1. Create a Student (`POST /students`)

**Request URL:** `http://127.0.0.1:8000/students`  
**Request Method:** `POST`  
**Request Body (JSON):**
```json
{
  "name": "Rahul Sharma",
  "date_of_birth": "2002-08-14",
  "email": "rahul.sharma@example.com",
  "phone": "9876543210",
  "course": "Computer Science Engineering",
  "address": "Sector 62, Noida, Uttar Pradesh",
  "enrollment_date": "2024-07-15"
}
```

**Response (`201 Created`):**
```json
{
  "id": 1,
  "name": "Rahul Sharma",
  "date_of_birth": "2002-08-14",
  "email": "rahul.sharma@example.com",
  "phone": "9876543210",
  "course": "Computer Science Engineering",
  "address": "Sector 62, Noida, Uttar Pradesh",
  "enrollment_date": "2024-07-15"
}
```

---

### 2. Retrieve All Students (`GET /students`)

**Request URL:** `http://127.0.0.1:8000/students`  
**Request Method:** `GET`  

**Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "name": "Rahul Sharma",
    "date_of_birth": "2002-08-14",
    "email": "rahul.sharma@example.com",
    "phone": "9876543210",
    "course": "Computer Science Engineering",
    "address": "Sector 62, Noida, Uttar Pradesh",
    "enrollment_date": "2024-07-15"
  }
]
```

---

### 3. Retrieve Student by ID (`GET /students/{student_id}`)

**Request URL:** `http://127.0.0.1:8000/students/1`  
**Request Method:** `GET`  

**Response (`200 OK`):**
```json
{
  "id": 1,
  "name": "Rahul Sharma",
  "date_of_birth": "2002-08-14",
  "email": "rahul.sharma@example.com",
  "phone": "9876543210",
  "course": "Computer Science Engineering",
  "address": "Sector 62, Noida, Uttar Pradesh",
  "enrollment_date": "2024-07-15"
}
```

---

### 4. Full Update (`PUT /students/{student_id}`)

**Request URL:** `http://127.0.0.1:8000/students/1`  
**Request Method:** `PUT`  
**Request Body (JSON):**
```json
{
  "name": "Rahul Sharma",
  "date_of_birth": "2002-08-14",
  "email": "rahul.sharma.new@example.com",
  "phone": "9876543210",
  "course": "Artificial Intelligence & ML",
  "address": "Sector 62, Noida, Uttar Pradesh",
  "enrollment_date": "2024-07-15"
}
```

**Response (`200 OK`):**
```json
{
  "id": 1,
  "name": "Rahul Sharma",
  "date_of_birth": "2002-08-14",
  "email": "rahul.sharma.new@example.com",
  "phone": "9876543210",
  "course": "Artificial Intelligence & ML",
  "address": "Sector 62, Noida, Uttar Pradesh",
  "enrollment_date": "2024-07-15"
}
```

---

### 5. Partial Update (`PATCH /students/{student_id}`)

**Request URL:** `http://127.0.0.1:8000/students/1`  
**Request Method:** `PATCH`  
**Request Body (JSON):** *(Only supplying course to update)*
```json
{
  "course": "Data Science & Analytics"
}
```

**Response (`200 OK`):**
```json
{
  "id": 1,
  "name": "Rahul Sharma",
  "date_of_birth": "2002-08-14",
  "email": "rahul.sharma.new@example.com",
  "phone": "9876543210",
  "course": "Data Science & Analytics",
  "address": "Sector 62, Noida, Uttar Pradesh",
  "enrollment_date": "2024-07-15"
}
```
*(Notice that name, dob, email, phone, and address remain intact without being overwritten!)*

---

### 6. Delete a Student (`DELETE /students/{student_id}`)

**Request URL:** `http://127.0.0.1:8000/students/1`  
**Request Method:** `DELETE`  

**Response (`200 OK`):**
```json
{
  "message": "Student with ID 1 was deleted successfully."
}
```

---

## 11. Example Error Responses

### Case 1: Student Not Found (`404 Not Found`)
Triggered when requesting an ID that does not exist:
```json
{
  "detail": "Student with ID 99999 was not found."
}
```

### Case 2: Missing Required Field (`422 Unprocessable Entity`)
Triggered when `name` or `date_of_birth` is omitted:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "name"],
      "msg": "Field required"
    }
  ]
}
```

### Case 3: Missing Both Email and Phone (`422 Unprocessable Entity`)
Triggered when neither contact method is supplied:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body"],
      "msg": "Value error, At least one of 'email' or 'phone' must be provided."
    }
  ]
}
```

### Case 4: Invalid Date Format (`422 Unprocessable Entity`)
Triggered when date is not in `YYYY-MM-DD` format (e.g. `14-08-2002`):
```json
{
  "detail": [
    {
      "type": "date_from_date_or_datetime_parsing",
      "loc": ["body", "date_of_birth"],
      "msg": "Input should be a valid date or date-time, input is too short"
    }
  ]
}
```

---

## 12. How SQLite Persistence Works

1. **Storage Location:** When the app starts, `database.py` locates its directory and connects to `students.db`.
2. **Auto-Initialization:** The function `init_db()` runs `CREATE TABLE IF NOT EXISTS students (...)`, ensuring the table is created immediately if missing.
3. **Disk Persistence:** SQLite commits every `INSERT`, `UPDATE`, and `DELETE` operation to the `students.db` file on disk.
4. **Surviving Restarts:** Even if you terminate Uvicorn (`Ctrl+C`) and start it again tomorrow, all student records remain safely preserved.

---

## 13. Running Automated Tests

A test script is included to automatically verify all 16 endpoint operations and validation edge cases:

```powershell
python test_api.py
```

Expected output:
```text
============================================================
STARTING API CRUD & VALIDATION TESTS
============================================================
[PASS] 1. Root endpoint GET / works.
[PASS] 2. POST /students created student with ID: 1
[PASS] 3. POST /students with only phone succeeded (ID: 2)
[PASS] 4. POST /students correctly rejected request missing both email and phone (422).
[PASS] 5. POST /students correctly rejected blank name (422).
[PASS] 6. POST /students correctly rejected invalid date format (422).
[PASS] 7. GET /students retrieved 2 student records.
[PASS] 8. GET /students/1 successfully retrieved student.
[PASS] 9. GET /students/999999 returned 404 Not Found.
[PASS] 10. PUT /students/1 updated all fields successfully.
[PASS] 11. PUT /students/999999 returned 404 Not Found.
[PASS] 12. PATCH /students/1 updated only specified fields.
[PASS] 13. PATCH /students/999999 returned 404 Not Found.
[PASS] 14. DELETE /students/1 deleted successfully.
[PASS] 15. GET /students/1 confirms student is deleted (404).
[PASS] 16. DELETE /students/1 for deleted record returned 404.
============================================================
ALL 16 TESTS PASSED SUCCESSFULLY! (100% WORKING)
============================================================
```

---

## 14. Uploading to GitHub

To submit this project to your GitHub repository:

### Step 1: Initialize Git Repository
```powershell
cd c:\Users\sadiya\Downloads\mis\student-crud-app
git init
```

### Step 2: Stage and Commit Files
```powershell
git add .
git commit -m "Initial commit: Complete Student Database CRUD Application"
```
*(The included `.gitignore` ensures that `venv/`, `students.db`, and `__pycache__/` will NOT be committed).*

### Step 3: Link to Your GitHub Repository & Push
```powershell
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/student-crud-app.git
git push -u origin main
```
