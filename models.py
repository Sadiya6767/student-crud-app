from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict


class StudentCreate(BaseModel):
    """
    Schema for creating a new student (POST /students) and full update (PUT /students/{id}).
    - 'name' and 'date_of_birth' are required.
    - At least one of 'email' or 'phone' must be provided.
    """
    name: str = Field(
        ...,
        min_length=1,
        description="Full name of the student",
        examples=["Rahul Sharma"]
    )
    date_of_birth: date = Field(
        ...,
        description="Date of birth in YYYY-MM-DD format",
        examples=["2002-08-14"]
    )
    email: Optional[str] = Field(
        None,
        description="Email address (optional if phone is provided)",
        examples=["rahul.sharma@example.com"]
    )
    phone: Optional[str] = Field(
        None,
        description="Phone number (optional if email is provided)",
        examples=["9876543210"]
    )
    course: Optional[str] = Field(
        None,
        description="Enrolled degree or course name",
        examples=["Computer Science"]
    )
    address: Optional[str] = Field(
        None,
        description="Residential address of the student",
        examples=["Sector 62, Noida, Uttar Pradesh"]
    )
    enrollment_date: Optional[date] = Field(
        None,
        description="Date of enrollment in YYYY-MM-DD format",
        examples=["2024-07-15"]
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Student name cannot be empty or whitespace only.")
        return cleaned

    @model_validator(mode="after")
    def validate_email_or_phone(self):
        # Clean email and phone strings
        email_clean = self.email.strip() if self.email and self.email.strip() else None
        phone_clean = self.phone.strip() if self.phone and self.phone.strip() else None

        self.email = email_clean
        self.phone = phone_clean

        # Validate that at least one contact method is present
        if not email_clean and not phone_clean:
            raise ValueError("At least one of 'email' or 'phone' must be provided.")

        # Basic email format check if email is provided
        if email_clean and ("@" not in email_clean or "." not in email_clean):
            raise ValueError("Invalid email format. Please provide a valid email address.")

        return self


class StudentUpdate(StudentCreate):
    """
    Schema for full update (PUT /students/{id}).
    Requires all mandatory fields, following standard PUT semantics.
    """
    pass


class StudentPatch(BaseModel):
    """
    Schema for partial update (PATCH /students/{id}).
    All fields are optional. Only fields provided by the client will be updated.
    """
    name: Optional[str] = Field(
        None,
        description="Updated full name of the student",
        examples=["Rahul Sharma"]
    )
    date_of_birth: Optional[date] = Field(
        None,
        description="Updated date of birth (YYYY-MM-DD)",
        examples=["2002-08-14"]
    )
    email: Optional[str] = Field(
        None,
        description="Updated email address",
        examples=["rahul.updated@example.com"]
    )
    phone: Optional[str] = Field(
        None,
        description="Updated phone number",
        examples=["9876543210"]
    )
    course: Optional[str] = Field(
        None,
        description="Updated course name",
        examples=["Information Technology"]
    )
    address: Optional[str] = Field(
        None,
        description="Updated address",
        examples=["Tower B, Sector 62, Noida"]
    )
    enrollment_date: Optional[date] = Field(
        None,
        description="Updated enrollment date (YYYY-MM-DD)",
        examples=["2024-07-15"]
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            cleaned = value.strip()
            if not cleaned:
                raise ValueError("Student name cannot be empty or whitespace only.")
            return cleaned
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            cleaned = value.strip()
            if cleaned and ("@" not in cleaned or "." not in cleaned):
                raise ValueError("Invalid email format. Please provide a valid email address.")
            return cleaned if cleaned else None
        return value


class StudentResponse(BaseModel):
    """
    Response schema for returning student data.
    Includes the auto-generated database ID.
    """
    id: int
    name: str
    date_of_birth: date
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)
