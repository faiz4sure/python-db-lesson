from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///management_system.sqlite')
Session = sessionmaker(bind=engine)

# Teacher Management Models
class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    join_date = Column(Date, default=datetime.now().date())
    password_hash = Column(String)
    students = relationship("Student", back_populates="teacher")

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    added_date = Column(Date, default=datetime.now().date())
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="students")
    attendance = relationship("Attendance", back_populates="student")
    grades = relationship("Grade", back_populates="student")

class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    date = Column(Date, nullable=False)
    status = Column(Boolean, default=False)  # True for present, False for absent
    student = relationship("Student", back_populates="attendance")

class Grade(Base):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    date = Column(Date, default=datetime.now().date())
    student = relationship("Student", back_populates="grades")

# Hospital Management Models
class Doctor(Base):
    __tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    specialization = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    password_hash = Column(String)
    patients = relationship("Patient", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")

class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    blood_group = Column(String)
    phone = Column(String)
    address = Column(String)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    doctor = relationship("Doctor", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    date = Column(Date, nullable=False)
    time_slot = Column(String, nullable=False)
    status = Column(String, default='Scheduled')  # Scheduled, Completed, Cancelled
    notes = Column(String)
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

class MedicalRecord(Base):
    __tablename__ = 'medical_records'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    diagnosis = Column(String, nullable=False)
    prescription = Column(String)
    notes = Column(String)
    date = Column(Date, default=datetime.now().date())
    patient = relationship("Patient", back_populates="medical_records")

# Create all tables
Base.metadata.create_all(engine)