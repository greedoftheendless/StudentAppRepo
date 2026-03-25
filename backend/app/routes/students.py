from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.metrics import STUDENT_CREATED_TOTAL, STUDENT_TOTAL_COUNT
from app.models import Student, User
from app.schemas import StudentCreate, StudentResponse

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def add_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    if db.query(Student).filter(Student.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    student = Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)

    STUDENT_CREATED_TOTAL.inc()
    STUDENT_TOTAL_COUNT.set(db.query(Student).count())

    return student


@router.get("/", response_model=list[StudentResponse])
def list_students(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return db.query(Student).order_by(Student.id).all()
