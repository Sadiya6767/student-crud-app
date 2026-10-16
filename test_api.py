"""
test_api.py - Verification script to test all CRUD endpoints and validation rules.
Run this using: python test_api.py
"""

import sys
from fastapi.testclient import TestClient
from main import app
from database import init_db

init_db()
client = TestClient(app)


def run_all_tests():
    print("=" * 60)
    print("STARTING API CRUD & VALIDATION TESTS")
    print("=" * 60)

    # 1. Test Root Endpoint
    res = client.get("/")
    assert res.status_code == 200, f"Root endpoint failed: {res.text}"
    print("[PASS] 1. Root endpoint GET / works.")

    # 2. Test POST /students (Valid student with email and phone)
    student_payload = {
        "name": "Aarav Sharma",
        "date_of_birth": "2002-05-15",
        "email": "aarav.sharma@example.com",
        "phone": "9876543210",
        "course": "Computer Science",
        "address": "Block C, Green Park, New Delhi",
        "enrollment_date": "2024-08-01"
    }
    res = client.post("/students", json=student_payload)
    assert res.status_code == 201, f"POST /students failed: {res.text}"
    created_student = res.json()
    assert "id" in created_student
    student_id = created_student["id"]
    assert created_student["name"] == "Aarav Sharma"
    print(f"[PASS] 2. POST /students created student with ID: {student_id}")

    # 3. Test POST /students with only phone (no email - valid because at least one is provided)
    res = client.post("/students", json={
        "name": "Priya Patel",
        "date_of_birth": "2003-09-10",
        "phone": "9812345678",
        "course": "Data Analytics"
    })
    assert res.status_code == 201, f"POST with only phone failed: {res.text}"
    priya_id = res.json()["id"]
    print(f"[PASS] 3. POST /students with only phone succeeded (ID: {priya_id})")

    # 4. Test POST /students validation: Missing BOTH email and phone -> Expect 422
    res = client.post("/students", json={
        "name": "Invalid Student",
        "date_of_birth": "2001-01-01"
    })
    assert res.status_code == 422, f"Expected 422 for missing contact info, got {res.status_code}"
    print("[PASS] 4. POST /students correctly rejected request missing both email and phone (422).")

    # 5. Test POST /students validation: Blank name -> Expect 422
    res = client.post("/students", json={
        "name": "   ",
        "date_of_birth": "2001-01-01",
        "email": "test@example.com"
    })
    assert res.status_code == 422, f"Expected 422 for blank name, got {res.status_code}"
    print("[PASS] 5. POST /students correctly rejected blank name (422).")

    # 6. Test POST /students validation: Invalid date of birth format -> Expect 422
    res = client.post("/students", json={
        "name": "Date Test",
        "date_of_birth": "15-05-2002",  # Wrong format, should be YYYY-MM-DD
        "email": "test@example.com"
    })
    assert res.status_code == 422, f"Expected 422 for invalid date, got {res.status_code}"
    print("[PASS] 6. POST /students correctly rejected invalid date format (422).")

    # 7. Test GET /students (Read all)
    res = client.get("/students")
    assert res.status_code == 200
    all_students = res.json()
    assert isinstance(all_students, list)
    assert len(all_students) >= 2
    print(f"[PASS] 7. GET /students retrieved {len(all_students)} student records.")

    # 8. Test GET /students/{id} (Read one)
    res = client.get(f"/students/{student_id}")
    assert res.status_code == 200
    retrieved = res.json()
    assert retrieved["id"] == student_id
    assert retrieved["name"] == "Aarav Sharma"
    assert retrieved["email"] == "aarav.sharma@example.com"
    print(f"[PASS] 8. GET /students/{student_id} successfully retrieved student.")

    # 9. Test GET /students/{id} with non-existent ID -> Expect 404
    res = client.get("/students/999999")
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"
    print("[PASS] 9. GET /students/999999 returned 404 Not Found.")

    # 10. Test PUT /students/{id} (Full update)
    put_payload = {
        "name": "Aarav S. Sharma",
        "date_of_birth": "2002-05-15",
        "email": "aarav.updated@example.com",
        "phone": "9876543210",
        "course": "Artificial Intelligence",
        "address": "Sector 18, Noida",
        "enrollment_date": "2024-08-01"
    }
    res = client.put(f"/students/{student_id}", json=put_payload)
    assert res.status_code == 200, f"PUT failed: {res.text}"
    updated_put = res.json()
    assert updated_put["name"] == "Aarav S. Sharma"
    assert updated_put["email"] == "aarav.updated@example.com"
    assert updated_put["course"] == "Artificial Intelligence"
    print(f"[PASS] 10. PUT /students/{student_id} updated all fields successfully.")

    # 11. Test PUT /students/{id} with non-existent ID -> Expect 404
    res = client.put("/students/999999", json=put_payload)
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"
    print("[PASS] 11. PUT /students/999999 returned 404 Not Found.")

    # 12. Test PATCH /students/{id} (Partial update - only change course)
    patch_payload = {
        "course": "Cloud Computing"
    }
    res = client.patch(f"/students/{student_id}", json=patch_payload)
    assert res.status_code == 200, f"PATCH failed: {res.text}"
    patched = res.json()
    # Check that course changed, but other fields remain untouched
    assert patched["course"] == "Cloud Computing"
    assert patched["name"] == "Aarav S. Sharma"
    assert patched["email"] == "aarav.updated@example.com"
    print(f"[PASS] 12. PATCH /students/{student_id} updated only specified fields.")

    # 13. Test PATCH /students/{id} with non-existent ID -> Expect 404
    res = client.patch("/students/999999", json=patch_payload)
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"
    print("[PASS] 13. PATCH /students/999999 returned 404 Not Found.")

    # 14. Test DELETE /students/{id}
    res = client.delete(f"/students/{student_id}")
    assert res.status_code == 200, f"DELETE failed: {res.text}"
    print(f"[PASS] 14. DELETE /students/{student_id} deleted successfully.")

    # 15. Verify student no longer exists after DELETE -> Expect 404
    res = client.get(f"/students/{student_id}")
    assert res.status_code == 404
    print(f"[PASS] 15. GET /students/{student_id} confirms student is deleted (404).")

    # 16. Test DELETE non-existent student -> Expect 404
    res = client.delete(f"/students/{student_id}")
    assert res.status_code == 404
    print(f"[PASS] 16. DELETE /students/{student_id} for deleted record returned 404.")

    print("=" * 60)
    print("ALL 16 TESTS PASSED SUCCESSFULLY! (100% WORKING)")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as e:
        print(f"[FAIL] Error running tests: {e}")
        sys.exit(1)
